import os
import unittest
from BSBolt.Simulate.SimulateMethylatedReads import SimulateMethylatedReads
from BSBolt.Utils.UtilityFunctions import reverse_complement, get_external_paths
from tests.TestHelpers import test_directory


bt2_path, art_path = get_external_paths()
# hold read simulation data to test functions

aln_pe_1_lines = [['>chr10	chr10-67760/1-1	67549	-',
                   'TAATTCAAGATTGCATTTTTCTGGGAGGTTTT-TAGATTTCAGCAACTAACAGCTGGGATTACAGGCGCCCACCACCACACCTGGCTAATTTTTGTATATTTTTTTTTGCCAAGCCCAAAGTCCAG',
                   'TAATTCAAGATTGCATTTTTCTGGGAGGTTTTGTAGATTTCAGCAACTAACAGCTGG-ATTACAGGCGCCCACCACCACGCCTGGCTAATTTTTGTATATTTTTTTTTGCCAAGCCCAAAGTCCAG'],
                  ['>chr10	chr10-67758/1-1	204153	-',
                   'ATTCACTATAGCAAATGGACATTTGGAGATCCCAAGAATGTCAAAGCGTTTTTGGTCATCTGTTATGGTAGCAC-AGTTGTTTTTCTACAGTAATCATGGTGAGAATGTAAATTAGTACAGCCATT',
                   'ATTCACTATAGCAAATGGACATTTGGAGATCCCAAGAATGTCAAAGCGTTTTTGGTCATCTGTTATGGTAGCACT-GTTGTTTTTCTACAGTAATCATGGTGAGAATGTAAATTAGTACAGCCATT'],
                  ['>chr10	chr10-67756/1-1	255075	-',
                   'CTGGAGACCACG-CATGGGCGACTGTGATGGGATCTCACTATGTTGCCCAGGTTGGTTTTAAACTCCTGGGCTCAACAACGGGAGAAAAACCACCTGCCGTGCTGCCAAGGCTGCGTCTCTTCATT',
                   'CTGGAGACCACGCCATGGGCGACTGTGATGGGATCTCACTATGTTGCCCAGGTTGGTTTTAAACTCCTGGGCTCAACAACGGGAGAAAAACCACCTGC-GTGCTGCCAAGGCTGCGTCTCTTCATT'],
                  ['>chr10	chr10-67754/1-1	281351	-',
                   'ACAGATAAAAGTCTCTTTGTCTCAACAAAATCTTAGTCCCATTATTTTATGGCAACATGGAAGACCTTA-TCCCTACTGAAAATAATTTTAAAATTAACCGGGCAGGCACCTGTAGTCCCAGCTAC',
                   'ACAGATAAAAGTCTCTTTGTCTCAACAAAATCTTAGTCCCATTATTTTATGGCAACATGGAAGACCTTAATCCCTACTGAAAATAATTTTAAAATTAACCGGGCAGGCACCTGTA-TCCCAGCTAC'],
                  ['>chr10	chr10-67752/1-1	253907	-',
                   'GTCCCTG-GCTCTAATTCTCATTGTCCCCAGGGTAGGACAGTAAAAAAGAGCCCACATTGCCAAGTTAATCCTAAGCCAAAAGAACAAAGCTGGAACATCAGCTTTCATGCCTCTGTTTTTGTTCT',
                   'GTCCCTGAGCTCTAATTCTCATTGTCCCCAGGG-AGGACAGTAAAAAAGAGCCCACATTGCCAAGTTAATCCTAAGCCAAAAGAACAAAGCTGGAACATCAGCTTTCATGCCTCTGTTTTTGTTCT'],
                  ['>chr10	chr10-67750/1-1	208626	+',
                   'CACCTGAGAATAGAAAACGCCCATGGATTAAGAAAACGTGCCACATATACACCATGGAATACTGTGCAGCCATAGCTTAAGCCACTGTTGATTTTTGTGACAGCTCAGTTGCTTAGAGC-AAGGTA',
                   'CACCTGAGAATAGAAAACGCCCATGGATTAAGAAAACGTGCCACATATACACCATGGAATACTGTGCAGCCAT-GCTTAAGCCACTGTTGATTTTTGTGACAGCTCAGTTGCTTAGAGCAAAGGTA'],
                  ['>chr10	chr10-67748/1-1	324914	-',
                   'ATGTACCTTGTGCTC-ACTTAAGTTTTTTAAAAAGAGTAACATGTTAACTCCATTTTGATTCTGAGAACTTTCACAATTTCTCCCTTTCAAACTTTCAGGCAGTGGGCTCCTCTGTGACGTAGGTC',
                   'ATGTACCTTGTGCTCTACTTAAGTTTTTTAAAAAGAGTAACATGTTAACT-CATTTTGATTCTGAGAACTTTCACAATTTCTCCCTTTCAAACTTTCAGGCAGTGGGCTCCTCTGTGACGTAGGTC'],
                  ['>chr10	chr10-67746/1-1	98695	-',
                   'TTCTGGCAGCAGAGAACTCCAATTCTGAAAATTCTGAACATGTGCTAATACCCTAGGTACCAATTTCTGGACTAGTCTGTTCTCACAT-TGCTATAATGAACTTCCAGCCACTGCGCCCAGTCCCC',
                   'TTCTGGCAGCAGAGAACTCCAA-TCTGAAAATTCTGAACATGTGCTAATACCCTAGGTACCAATTTCTGGACTAGTCTGTTCTCACATCTGCTATAATGAACTTCCAGCCACTGCGCCCAGTCCCC'],
                  ['>chr10	chr10-67744/1-1	198975	-',
                   'TCTGTTTGTTAGTTTTCCTTCTAACGAGGAGGATCT-AGTCCCTCCTGCTGTCCTACCACATGGAGCACCCCACACACGCTCATTTCAGAAATGTGGGCCTGACTGAAATCATTAGGTTCACAAAA',
                   'TCTGTTTGTTAGTTTTCCTTCTAACGA-GAGGATCTGAGTCCCTCCTGCTGTCCTACCACATGGAGCACCCCACACACGCTCATTTCAGAAATGTGGGCCTGACTGAAATCATTAGGTTCACAAAA'],
                  ['>chr10	chr10-67742/1-1	345817	-',
                   'GCAACAAAATATATATTTGTCTTCCCTGATTGTCTCACTCACTGAAACTGGCAATTTAAGTCAGTGTGGCGATTCCTCAGGGAT-CTTGCTCTGTCACCCAGGCTGGAGTGCAGTGCTACAATCTC',
                   'GCAACAAAATATATATTTG-CTTCCCTGATTGTCTCACTCACTGAAACTGGCAATTTAAGTCAGTGTGGCGATTCCTCAGGGATCCTTGCTCTGTCACCCAGGCTGGAGTGCAGTGCTACAATCTC']]

aln_pe_2_lines = [['>chr10	chr10-67760/2	355545	+',
                   'CCTCTTTTCCCCAAAGGACCACAGGGAATCCCGTAGTTGAGTAAATAAACAGTGATTTTCCAATCTACCCATCTGACAAAGGGCTAATATCCAGAATCTACAAAGCAGCTGGTGATTGGTCATTG',
                   'CCTCTTTTCCCCAAAGGACCACAGGGAATCCCGTAGTTGAGTAAATAAACAGTGATTTTCCAATCTACCCATCTGACAAAGGGCTAATATCCAGAATCTACAAAGCAGCTGGTGATTGGTCATTG'],
                  ['>chr10	chr10-67758/2	218952	+',
                   'GGTGGAAGTGGGGATTGCCAACACGTAGCCCGCAGGCTGACAGAGGCTGCTTTGTCAGATGGATGGAGTCTGAATGGCAGTTACTTAAAAAGTCAAGAAACAGTCCTTGGCGTAGAAATAACAGG',
                   'GGTGGAAGTGGGGATTGCCAACACGTAGCCCGCAGGCTGACAGAGGCTGCTTTGTCAGATGGATGGAGTCTGAATGGCAGTTACTTAAAAAGTCAAGCAACAGTCCTTGGCGTAGAAATAACAGG'],
                  ['>chr10	chr10-67756/2	167942	+',
                   'CCATCCTGGGTTTTCTGCCTTTCTCCTTCCTGTTGTATCGTGAGGACAGCCTCTTTTCGGGTCTCACTCTGTCACCCAGGCTGAAGTGCAATGGCTTGATTATTGCTCTTAATCGAGCAGTTTGG',
                   'CCATCCTGGGTTTTCTGCCTTTCTCCTTCCTGTTGTATCGTGAGGACAGCCTCTTTTCGGGTCTCACTCTGTCACCCAGGCTGAAGTGCAATGGCTTGATTATTGCTCTTAATCGAGCAGTTTGG'],
                  ['>chr10	chr10-67754/2	141713	+',
                   'CACACACACACACACACAAACACACATAATGCAAACATACACCATGGTTTTAGAGGGAGGAAGCTCACAGCCTACTCAGAGTTTCCAACACACTGTTTATTCAGCATCCCCAAGGGGAAAAAAGA',
                   'CACACACACACACACACAAACACACATAATGCAAACATACACCATGGTTTTAGAGGGAGGAAGCTCACAGCCTACTCAGAGTTTCCAACACACTGTTTATTCAGCATCCCCAAGGGGAAAAAAGA'],
                  ['>chr10	chr10-67752/2	169144	+',
                   'CCCATGTAGTTTTTTGAGGAACTTTCATATGGTTTCCATGGCTGTATTAACTCACAATTTACCTATGTAACAAACCTGCACATCTGCACATGTACCCCAGAACTTATCTCAAACTTCTGGACTCA',
                   'CCCATGTAGTTTTTTGAGGAACTTTCATATGGTTTCCATGGCTGTATTAACTCACAATTTACCTATGTAACAAACCTGCACATCTGCACATGTACCCCAGAACTTATCTCAAACTTCTGGACTCA'],
                  ['>chr10	chr10-67750/2	214538	-',
                   'AGGTGTTTCATTTTTTATTTCCTTGAGCAGCGGTTTGTAGTTCTCCTTGAAGAGGTCCTTCATTCTCTCAACCATTCATCATTGAATTTGGTGGCTGAAAAGAAATTTTAAGTTGACAATGTGTT',
                   'AGGTGTTTCATTTTTTATTTCCTTGAGCAGCGGTTTGTAGTTCTCCTTGAAGAGGTCCTTCATTCTCTCAACCATTCATCATTGAATTTGGTGGCTGAAAAGAAATTTTAAGTTGACAATGTGTT'],
                  ['>chr10	chr10-67748/2	98306	+',
                   'TTTGTTTCTTTGCCATTTGTTTTCGAATGGGTGTGGCATTGCTTCACTGCAACCTCTGCCTCCCAGGTTCAAGTGATTCTCCTACCTCGGCCTCTGATATTTGCTCAAACATCTTGTAAACTGTA',
                   'TTTGTTTCTTTGCCATTTGTTTTCGAATGGGTGTGGCATTGCTTCACTGCAACCTCTGCCTCCCAGGTTCAAGTGATTCTCCTACCTCGGCCTCTGATATTTGCTCAAACATCTTGTAAACTGTA'],
                  ['>chr10	chr10-67746/2	324439	+',
                   'GTGGCCACATGCTGCTTAGTGTCTTATATGGCCAGTGATAATGTCTGTGAGAGCGCAGACTAAGAAACAAAATCCAACACAAAATCAGGAAGGGGCCACCTAAGAGATAAGTATAAAAACTACAC',
                   'GTGGCCACATGCTGCTTAGTGTCTTATATGGCCAGTGATAATGTCTGTGAGAGCGCAGACTAAGAAACAAAATCCAACACAAAATCAGGAAGGGGCCACCTAAGAGATAAGTATAAAAACTACAC'],
                  ['>chr10	chr10-67744/2	224127	+',
                   'GCTCATATGAGCAATGAATCAATATAAGAGACACAGAGTAAGAACCTAAGTTATCACCTTGATTCAGTAACAACAAAGAGTCAGGGGCCTGGCACATCAGTGAAGCTGCCAGTTCAAGAACTAGT',
                   'GCTCATATGAGCAATGAATCAATATAAGAGACACAGAGTAAGAACCCAAGTTATCACCTTGATTCAGTAACAACAAAGAGTCAGGGGCCTGGCACATCAGTGAAGCTGCCAGTTCAAGAACTAGT'],
                  ['>chr10	chr10-67742/2	77239	+',
                   'CGTGAACCCGGCCTGGTTCCATCTCCCCCGTCTCTGGAGAGGCCCTGCATCCTTCTCCCCCGGAATGGGAACCTGAGTCAAGGAGGCCAGTGGGGCAGCCTGGCACCAGGACCATAATTTCCACA',
                   'CGTGAACCCGGCCTGGTTCCATCTCCCCCGTCTCTGGAGAGGCCGTGCATCCTTCTCCCCCGGAATGGGAACCTGAGTCAAGGAGGCCAGTGGGGCAGCCTGGCACCAGGACCATAATTTCCACA']]

sam_lines = [
    'chr10-67760	83	chr10	355827	99	68M1D24M1I32M	=	355546	-406	CTGGACTTTGGGCTTGGCAAAAAAAAATATACAAAAATTAGCCAGGCGTGGTGGTGGGCGCCTGTAATCCAGCTGTTAGTTGCTGAAATCTACAAAACCTCCCAGAAAAATGCAATCTTGAATTA	GGGG>GGGGGDGGGGGG1G.FGGGGGG0EG.GGGGGGGGGGGDGGGG>FGGGGEDGGGGGGGFGG1GGGGGGGGGBGGGGGGFG>GGBG>GGGGGGG=G<GGGGGGEGE>GGGGGGG1GGBCC?B',
    'chr10-67760	163	chr10	355546	99	125M	=	355827	406	CCTCTTTTCCCCAAAGGACCACAGGGAATCCCGTAGTTGAGTAAATAAACAGTGATTTTCCAATCTACCCATCTGACAAAGGGCTAATATCCAGAATCTACAAAGCAGCTGGTGATTGGTCATTG	BCACBGGGGGEGGBGGFGGGGGEGFGGGGG1GGGGCGGGG1GGFGGGGF1GGGGC:GGGGGGGGCGGGGG0GGEDGG:GG/GGEGGGGGCGGGGGGF.GGGDFGGGG;CG=BGEGGGGGG=GGGG',
    'chr10-67758	83	chr10	219223	99	50M1D1I74M	=	218953	-395	AATGGCTGTACTAATTTACATTCTCACCATGATTACTGTAGAAAAACAACAGTGCTACCATAACAGATGACCAAAAACGCTTTGACATTCTTGGGATCTCCAAATGTCCATTTGCTATAGTGAAT	GGGG8GDGGFGGGGDGEGFG.GG8G<0EEG8GGG@@GGGFGGEGGGGGGGGGFGG0GGGGGGGGGGGGFG:GGGGGGGGDGGGGGFGGGGGGGGGF/GGG;GFGGGGGBGGGGGGGG1FGCCCCB',
    'chr10-67758	163	chr10	218953	99	125M	=	219223	395	GGTGGAAGTGGGGATTGCCAACACGTAGCCCGCAGGCTGACAGAGGCTGCTTTGTCAGATGGATGGAGTCTGAATGGCAGTTACTTAAAAAGTCAAGCAACAGTCCTTGGCGTAGAAATAACAGG	CCBBCGGGG0GGG<GGGGGGGGGGGGGGGGGGGEEGGGGGGGFGGGGGGG:GGGGGGGGDG0G:GGGGGGGDBGGGGGGGGGFG>GGG0>GGGGGGG#GGGFGG0GGGG@GDGGFGGGGG8GGG@',
    'chr10-67756	83	chr10	168301	99	27M1D85M1I12M	=	167943	-483	AATGAAGAGACGCAGCCTTGGCAGCACGCAGGTGGTTTTTCTCCCGTTGTTGAGCCCAGGAGTTTAAAACCAACCTGGGCAACATAGTGAGATCCCATCACAGTCGCCCATGGCGTGGTCTCCAG	GGGGC@CGGGGG6GGGEGG>E0GGGG/GGGG0GGGGGG>G@GGGGDG1/GGGFGGGGGEFG/GGGG1GBEGF:GGGGGGGGGGGGGGGGGGGGGGGFGGGGGEFGF;GGCGGGGGG1FEBCBBBC',
    'chr10-67756	163	chr10	167943	99	125M	=	168301	483	CCATCCTGGGTTTTCTGCCTTTCTCCTTCCTGTTGTATCGTGAGGACAGCCTCTTTTCGGGTCTCACTCTGTCACCCAGGCTGAAGTGCAATGGCTTGATTATTGCTCTTAATCGAGCAGTTTGG	CCC@CGGGG>GGGGG1G1GEGGGGGGGGGB:CGGGGGGGGGCEGG<GGGGG/GG1GGG9GFGDG/GGGGG:GGGGG@GGG<CGGGFG1GGGGGGGG0GGGDGGGCGG0CGGGGGDGGGGGGGGG6',
    'chr10-67754	83	chr10	142025	99	10M1D45M1I69M	=	141714	-436	GTAGCTGGGATACAGGTGCCTGCCCGGTTAATTTTAAAATTATTTTCAGTAGGGATTAAGGTCTTCCATGTTGCCATAAAATAATGGGACTAAGATTTTGTTGAGACAAAGAGACTTTTATCTGT	G9GCD=GGG0GGEGG/GG>FG>G0GGG:GGGDGGG>;GGGEGGGGGGFGGGGGGGGGGGGGGEGGGGGGGGGGG1F/GGGGCGGGFGGGF1CGG1G:GGGGGGFGGGGGGGGGDGGGGGECCBBB',
    'chr10-67754	163	chr10	141714	99	125M	=	142025	436	CACACACACACACACACAAACACACATAATGCAAACATACACCATGGTTTTAGAGGGAGGAAGCTCACAGCCTACTCAGAGTTTCCAACACACTGTTTATTCAGCATCCCCAAGGGGAAAAAAGA	:BCC0GGGGGGGGGGGG>GGGGGGG<GGGGGC1GGEGGGGGGGFG>G11G<GGGGGGGGGGGGGGGGGFEGCGGCFGG0=GGGGGGGCGFGBGGDGGGDGGG8FGGGGGGG:@GEG8GF>GGGEG',
    'chr10-67752	83	chr10	169469	99	92M1D25M1I7M	=	169145	-449	AGAACAAAAACAGAGGCATGAAAGCTGATGTTCCAGCTTTGTTCTTTTGGCTTAGGATTAACTTGGCAATGTGGGCTCTTTTTTACTGTCCTCCCTGGGGACAATGAGAATTAGAGCTCAGGGAC	G@GGC@FGDGGGGDGGGF/G>BGG8GGGD>GGFGGGGG.GGGG/CG/GGGGGGGGGGBGGGGEGGGGGEGGGGGGGGGGGDFGGGGGGBGGGGGGGGGGGGGGFGF1G=GGG@DGEGFGECCACC',
    'chr10-67752	163	chr10	169145	99	125M	=	169469	449	CCCATGTAGTTTTTTGAGGAACTTTCATATGGTTTCCATGGCTGTATTAACTCACAATTTACCTATGTAACAAACCTGCACATCTGCACATGTACCCCAGAACTTATCTCAAACTTCTGGACTCA	CBBBCGGGGGGGGGGGGGFGGGGGGGGGGG:GGGGGGCGGGGGGGBGGCGEG1GEGGGGGG@GGEGGGGGGGCGGEEGFGGGGGGBGGGGGGGGGGGGG8GGGGEGG.GGG.GGGG=GGGGEGBG',
    'chr10-67750	99	chr10	208627	99	73M1D45M1I6M	=	208838	336	CACCTGAGAATAGAAAACGCCCATGGATTAAGAAAACGTGCCACATATACACCATGGAATACTGTGCAGCCATGCTTAAGCCACTGTTGATTTTTGTGACAGCTCAGTTGCTTAGAGCAAAGGTA	BC3CAGGGGGGGGGGGGFGGGGGGGG0GGGGGGGGGEGGGGG/GGGGGGCGGGGGG=1FGGCGGGGGGGGGGGGFDGGDGGGGGGGGGGGGFGGGGGGGFGGGGGGGGE1EGECGGG;GG0GGF=',
    'chr10-67750	147	chr10	208838	99	125M	=	208627	-336	AACACATTGTCAACTTAAAATTTCTTTTCAGCCACCAAATTCAATGATGAATGGTTGAGAGAATGAAGGACCTCTTCAAGGAGAACTACAAACCGCTGCTCAAGGAAATAAAAAATGAAACACCT	GGGGGGFGGGGGGGG.GGGCG0GGGG0GGFGGGGGGG1GG=GGBFGGGGGGGGGFGGGGGGGGGGG@FG1E=GGGGGGGGGGGGGG:1GFGG1GG9GGGGGG1>GGGGGGGGGGGGGGGGAC@BB',
    'chr10-67748	83	chr10	98462	99	75M1D34M1I15M	=	98307	-280	GACCTACGTCACAGAGGAGCCCACTGCCTGAAAGTTTGAAAGGGAGAAATTGTGAAAGTTCTCAGAATCAAAATGAGTTAACATGTTACTCTTTTTAAAAAACTTAAGTAGAGCACAAGGTACAT	GGGBDCDGAGCGGGGGF10GGGG=GGGGGGEGGGGGFGGGGGGFGGGGFGGFGGGGE1GFGGG@GGGGGGGG/GGGGGGCGGGGGCGGGGGGFCGFGB>GGGGCGGGGGGGG;CGGFGGECCB3<',
    'chr10-67748	163	chr10	98307	99	125M	=	98462	280	TTTGTTTCTTTGCCATTTGTTTTCGAATGGGTGTGGCATTGCTTCACTGCAACCTCTGCCTCCCAGGTTCAAGTGATTCTCCTACCTCGGCCTCTGATATTTGCTCAAACATCTTGTAAACTGTA	CBB@BGGGGGGGEGGGGC=G/GGGGGGGCGGGGGGEG=DGGGGGBGGGEGC>G>GGGGGGGG1GGGG>G/GGGGG<GGCGG/GG>GGGGGFGGGB1GGGGFGGGGGG=GGGGGGG/GGGGGGG/G',
    'chr10-67746	83	chr10	324681	99	37M1I65M1D22M	=	324440	-366	GGGGACTGGGCGCAGTGGCTGGAAGTTCATTATAGCAGATGTGAGAACAGACTAGTCCAGAAATTGGTACCTAGGGTATTAGCACATGTTCAGAATTTTCAGATTGGAGTTCTCTGCTGCCAGAA	GBEGDGGGGGGGGGGGFEGBGGGGG:G>FGFGGGGGGEG0GGGGGGEGGGGGGGFCGGGGGG0GGGFGGGGGGGGGG<GGGGGGGGGGGDGGGGGGGCGGGGGGGGGGGGGGGGGGGGGFCACCB',
    'chr10-67746	163	chr10	324440	99	125M	=	324681	366	GTGGCCACATGCTGCTTAGTGTCTTATATGGCCAGTGATAATGTCTGTGAGAGCGCAGACTAAGAAACAAAATCCAACACAAAATCAGGAAGGGGCCACCTAAGAGATAAGTATAAAAACTACAC	BC:BCEGGGGGDGGGGGGGDGDDEGGGG1GBG>1GGGGGGGGG/1GE1GGGGGGGGGGGGGG>GGG<GGGGEGGGGDG1GGGGGGGGGGGGGGD<GGGGGGG:GGGGGFGG9GGFGGGFGDG6GG',
    'chr10-67744	83	chr10	224401	99	89M1I8M1D27M	=	224128	-398	TTTTGTGAACCTAATGATTTCAGTCAGGCCCACATTTCTGAAATGAGCGTGTGTGGGGTGCTCCATGTGGTAGGACAGCAGGAGGGACTCAGATCCTCTCGTTAGAAGGAAAACTAACAAACAGA	GGGGGGGGB/GGGGGGGGG>GGGGGGGGGBDGGGGGEGGGGGGGGGG:GGCGGGGGCGGDGE0EGG@@GGGGGGGGGGGGGGGGGGGG1GGGGGGGFGGGGBGGGGGGCGGGGGGG1GGGBBBCC',
    'chr10-67744	163	chr10	224128	99	125M	=	224401	398	GCTCATATGAGCAATGAATCAATATAAGAGACACAGAGTAAGAACCCAAGTTATCACCTTGATTCAGTAACAACAAAGAGTCAGGGGCCTGGCACATCAGTGAAGCTGCCAGTTCAAGAACTAGT	:C:BCGGGGGGGGGGGE<;GFGC=G@GGEGCCGGGGGGGGGGGFGG1G1GGGBFFGEGGG1GGGGGGDGGGGG<GGEGGGF00GGGGGGGGGGGGDF>FGCGG0GDGGGGG00GDGG.GGGG.GG',
    'chr10-67742	83	chr10	77559	99	41M1I64M1D19M	=	77240	-444	GAGATTGTAGCACTGCACTCCAGCCTGGGTGACAGAGCAAGGATCCCTGAGGAATCGCCACACTGACTTAAATTGCCAGTTTCAGTGAGTGAGACAATCAGGGAAGCAAATATATATTTTGTTGC	GGGGDGGGGGGEGGDGGGGGCGG@GGEGGG0G0FGF.BGGGGGGGG>G1GFGGGGGGGGDGGGBGGGCGGGGGGGGGGGGCG1GGGGGGGGGGGG>=GGG/GFG1G;GGGGGGGFGGGGGCBCCB',
    'chr10-67742	163	chr10	77240	99	125M	=	77559	444	CGTGAACCCGGCCTGGTTCCATCTCCCCCGTCTCTGGAGAGGCCGTGCATCCTTCTCCCCCGGAATGGGAACCTGAGTCAAGGAGGCCAGTGGGGCAGCCTGGCACCAGGACCATAATTTCCACA	@3BABGGEDGG@GGGGGGG@GGDGG=GG/GGGGCGGGGGGGGGG/FGG@GG1GGG>GGGF/GGGGGGGGBEGGGGGGCGGGGGGFGGEGGEGGDGGGGGGG.GGE0GFGFGGGGCGG@GGGGGGG']

simulation_files = f'{test_directory}/TestSimulations/wgbs_pe'
test_genome = f'{test_directory}/TestData/BSB_test.fa'

test_simulation_files = SimulateMethylatedReads(reference_file=test_genome,
                                                art_path=art_path,
                                                paired_end=True,
                                                output_path=simulation_files,
                                                methylation_reference_output=f'{simulation_files}/wgbs_pe_ref/test',
                                                undirectional=False)
test_simulation_files.run_simulation()

# combine aln lines
all_aln_lines = []
for aln1, aln2 in zip(aln_pe_1_lines, aln_pe_2_lines):
    all_aln_lines.append(aln1)
    all_aln_lines.append(aln2)


class TestReadSimulation(unittest.TestCase):

    def setUp(self):
        pass

    def test_read_index_conversion(self):
        # ensure read index conversion if read is on - strand
        for aln_line, sam_line in zip(all_aln_lines, sam_lines):
            # aln files are zero indexed and sam files are one indexed so remove 1 from position
            sam_position = int(sam_line.split('\t')[3]) - 1
            aln_profile: dict = test_simulation_files.parse_aln_line(aln_line)
            self.assertEqual(sam_position, aln_profile['read_index'])

    def test_read_output(self):
        # aligned sam sequence should match
        for aln_line, sam_line in zip(all_aln_lines, sam_lines):
            sam_read = sam_line.split('\t')[9]
            aln_profile: dict = test_simulation_files.parse_aln_line(aln_line)
            test_fastq_line = [None, None, None, None]
            methylation_strand = 'Watson'
            read_sequence = test_simulation_files.set_simulated_methylation(aln_profile,
                                                                            test_fastq_line,
                                                                            methylation_strand)[1]
            # only G should be mofied on - strand and only C on + strand
            if aln_profile['reference_strand'] == '-':
                self.assertEqual(reverse_complement(read_sequence.replace('g', 'G')), sam_read)
            else:
                self.assertEqual(read_sequence.replace('c', 'C'), sam_read)

    def test_methylation_setting(self):
        aln_profile: dict = test_simulation_files.parse_aln_line(all_aln_lines[1])
        watson_changes = [1, 72]
        watson_dict = {'chr10:355546': ['C', 1, 'CG', 0, 0],
                       'chr10:355617': ['C', 1, 'CG', 0, 0]}
        crick_changes = [15, 93]
        crick_dict = {'chr10:355560': ['G', 1, 'GC', 0, 0],
                      'chr10:355638': ['G', 1, 'GC', 0, 0]}
        test_simulation_files.cytosine_dict = {'Watson': watson_dict, 'Crick': crick_dict}
        test_simulation_files.current_contig = 'chr10'

        test_fastq_line = [None, None, None, None]
        methylation_strand = 'Watson'
        read_sequence = test_simulation_files.set_simulated_methylation(aln_profile,
                                                                        test_fastq_line,
                                                                        methylation_strand)[1]
        for site in watson_changes:
            self.assertEqual(read_sequence[site], 'c')
        test_fastq_line = [None, None, None, None]
        methylation_strand = 'Crick'
        read_sequence = test_simulation_files.set_simulated_methylation(aln_profile,
                                                                        test_fastq_line,
                                                                        methylation_strand)[1]
        for site in crick_changes:
            self.assertEqual(read_sequence[site], 'g')


if __name__ == '__main__':
    unittest.main()
