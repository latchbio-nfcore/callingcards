
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'min_mapq': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title='Hops counting options',
        description='Values with less than or equal to this mapq value will not be counted as transpositions. Defaults to 10',
    ),
    'aligner': NextflowParameter(
        type=typing.Optional[str],
        default='bwamem2',
        section_title='Alignment options',
        description='Choose one of the configured aligners. Defaults to bwamem2.',
    ),
    'r1_bc_pattern': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Read processing options',
        description='UMITools compliant read 1 barcode pattern. See UMITools documentation',
    ),
    'r2_bc_pattern': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='UMITools compliant read 2 barcode pattern. See UMITools documentation',
    ),
    'r1_crop': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='If reads are single_end, this option allows the user to crop the R1 read. This occurs after trimming',
    ),
    'split_fastq_by_size': NextflowParameter(
        type=typing.Optional[int],
        default=None,
        section_title=None,
        description='split_fastq_by_size or split_fastq_by_part may be set, but not both at the same time. These parameters control how many parts the input fastq files are split into for parallel processing on a cluster. See seqkit split2 for more information. By default, split_fastq_by_part is set to 10, which will split every fastq file into 10 parts. If you wish to use split_fastq_by_size, set split_fastq_by_part to null to nullify the default value.',
    ),
    'split_fastq_by_part': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='split_fastq_by_size or split_fastq_by_part may be set, but not both at the same time. These parameters control how many parts the input fastq files are split into for parallel processing on a cluster. See seqkit split2 for more information. By default, split_fastq_by_part is set to 10, which will split every fastq file into 10 parts. If you wish to use split_fastq_by_size, set split_fastq_by_part to null to nullify the default value.',
    ),
    'datatype': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description="This determines which workflow to run based on the organism and method from which the data originates. Current options are 'yeast' and 'mammals'",
    ),
    'input': NextflowParameter(
        type=LatchFile,
        default=None,
        section_title=None,
        description='Path to comma-separated file containing information about the samples in the experiment.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Reference genome options',
        description='Name of iGenomes reference.',
    ),
    'fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Path to FASTA genome file.',
    ),
    'gtf': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to GTF annotation file.',
    ),
    'regions_mask': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='A bed file which specifies regions to hard mask in genome fasta',
    ),
    'additional_fasta': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Additional sequences which will be appended to the genomic fasta file after masking',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
}

