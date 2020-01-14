import gzip
import pickle
import subprocess
import unittest

from BSBolt.Utils.AlignmentEvaluation import AlignmentEvaluator, get_alignments
from tests.TestHelpers import bsb_directory, z_test_of_proportion


# generate simulated reads
bsb_simulate_commands = ['python3', '-m', 'BSBolt', 'Simulate',
                         '-G', f'{bsb_directory}tests/TestData/BSB_test.fa',
                         '-O', f'{bsb_directory}tests/TestSimulations/BSB_pe', '-PE', '-IR1', '0.01',
                         '-IR2', '0.01', '-DR1', '0.01', '-DR2', '0.01', '-U']
subprocess.run(bsb_simulate_commands)

print('Reads Simulated')
# map simulated reads

print('Building Methylation Index')
bsb_index_commands = ['python3', '-m', 'BSBolt', 'Index', '-G', f'{bsb_directory}tests/TestData/BSB_test.fa',
                      '-DB', f'{bsb_directory}tests/TestData/BSB_Test_DB']
subprocess.run(bsb_index_commands)
print('BSBolt Index Built')


bsb_align_commands = ['python3', '-m', 'BSBolt', 'Align',
                      '-DB', f'{bsb_directory}tests/TestData/BSB_Test_DB', '-F1',
                      f'{bsb_directory}tests/TestSimulations/BSB_pe_meth_1.fastq', '-F2',
                      f'{bsb_directory}tests/TestSimulations/BSB_pe_meth_2.fastq', '-O',
                      f'{bsb_directory}tests/BSB_pe_test', '-S', '-BT2-k', '10', '-BT2-p', '10', '-discord']

subprocess.run(bsb_align_commands)

print('Calling Methylation')

bs_call_methylation_args = ['python3', '-m', 'BSBolt', 'CallMethylation', '-I',
                            f'{bsb_directory}tests/BSB_pe_test.sorted.bam',
                            '-O', f'{bsb_directory}tests/BSB_pe_test',
                            '-DB', f'{bsb_directory}tests/TestData/BSB_Test_DB',
                            '-t', '6', '-verbose', '-min-qual', '10']
subprocess.run(bs_call_methylation_args)
print('Methylation Values Called')

# retrieve reference and test alignments
reference_alignments = get_alignments(f'{bsb_directory}tests/TestSimulations/BSB_pe.sam')
test_alignments = get_alignments(f'{bsb_directory}tests/BSB_pe_test.sorted.bam')

evaluator = AlignmentEvaluator(duplicated_regions={'chr10': (0, 5000), 'chr15': (0, 5000)},
                               matching_target_prop=.95)

print('Evaluating Alignment')
read_stats = evaluator.evaluate_alignment(reference_alignments, test_alignments)

# import methylation calling dict
print('Evaluating Methylation Calls')
all_methylation_sites = {}

output_chromosome = ['chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15']
for chrom in output_chromosome:
    with open(f'{bsb_directory}tests/TestSimulations/BSB_pe.{chrom}.pkl', 'rb') as sim_sites:
        chrom_sites = pickle.load(sim_sites)
        all_methylation_sites.update(chrom_sites['Watson'])
        all_methylation_sites.update(chrom_sites['Crick'])

# import CGmap Calls
cgmap_sites = {}

for line in gzip.open(f'{bsb_directory}tests/BSB_pe_test.CGmap.gz', 'rb'):
    processed_line = line.decode('utf-8').replace('\n', '').split('\t')
    cgmap_sites[f'{processed_line[0]}:{int(processed_line[2]) - 1}'] = dict(nucleotide=processed_line[1],
                                                                            methylation_level=processed_line[5],
                                                                            context=processed_line[4],
                                                                            methylated_reads=processed_line[6],
                                                                            total_reads=processed_line[7])


# get line comparisons

site_comparisons = {}
for site, cgmap_values in cgmap_sites.items():
    site_comparison = dict(coverage_difference=0, simulation_beta=0, mapped_beta=0, beta_z_value=0)
    cgmap_site_coverage = int(cgmap_values['total_reads'])
    reference_values = all_methylation_sites[site]
    reference_coverage = int(reference_values[3]) + int(reference_values[4])
    site_comparison['coverage_difference'] = abs(cgmap_site_coverage - reference_coverage)
    site_comparison['simulation_beta'] = reference_values[1]
    site_comparison['mapped_beta'] = cgmap_values['methylation_level']
    cgmap_meth = int(cgmap_sites[site]['methylated_reads'])
    cgmap_unmeth = int(cgmap_sites[site]['total_reads']) - int(cgmap_sites[site]['methylated_reads'])
    ref_meth = int(reference_values[3])
    ref_unmeth = int(reference_values[4])
    z = abs(z_test_of_proportion(a_yes=cgmap_meth, a_no=cgmap_unmeth, b_yes=ref_meth, b_no=ref_unmeth))
    site_comparison['beta_z_value'] = z
    site_comparisons[site] = site_comparison


class TestBSBPipeline(unittest.TestCase):
    """ The first 5000bp for chr10 are duplicated as chr15 in the simulation reference. These regions will have
    mixed methylation values and coverage values"""

    def setUp(self):
        pass

    def test_read_coverage(self):
        # set coverage difference between simulated and mapped reads to consider site out of tolerance
        coverage_difference_tolerance = 5
        # count number of sites out of tolerance
        out_of_tolerance_sites = 0
        for label, test_site in site_comparisons.items():
            chromosome, pos = label.split(':')
            if chromosome in {'chr10', 'chr15'} and int(pos) < 5000:
                continue
            if test_site['coverage_difference'] > coverage_difference_tolerance:
                out_of_tolerance_sites += 1
        self.assertLessEqual(out_of_tolerance_sites, 5)

    def test_beta_proportion(self):
        # set z threshold
        z_threshold = 3
        # count site with z score above threshold
        z_site_count = 0
        for label, test_site in site_comparisons.items():
            chromosome, pos = label.split(':')
            if chromosome in {'chr10', 'chr15'} and int(pos) < 5000:
                continue
            if test_site['beta_z_value'] >= z_threshold:
                z_site_count += 1
        self.assertLessEqual(z_site_count, 5)

    def test_read_alignments(self):
        # asses proportion of reads that mapped to simulated region
        on_target_alignments = read_stats['on_target_paired'] + read_stats['on_target_single']
        off_target_alignments = read_stats['off_target_paired'] + read_stats['off_target_single']
        self.assertGreater(on_target_alignments / read_stats['total_alignments'],  0.95)
        self.assertLess(off_target_alignments / read_stats['total_alignments'], 0.01)
        self.assertLess(read_stats['unaligned'] / read_stats['total_alignments'], 0.03)


if __name__ == '__main__':
    unittest.main()
