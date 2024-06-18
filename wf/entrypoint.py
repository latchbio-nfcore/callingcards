from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, r1_bc_pattern: typing.Optional[str], r2_bc_pattern: typing.Optional[str], r1_crop: typing.Optional[int], split_fastq_by_size: typing.Optional[int], datatype: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], gtf: typing.Optional[str], regions_mask: typing.Optional[LatchFile], additional_fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], min_mapq: typing.Optional[int], aligner: typing.Optional[str], split_fastq_by_part: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
            "nextflow",
            ".nextflow",
            "work",
            "results",
            "miniconda",
            "anaconda3",
            "mambaforge",
        ]

        shutil.copytree(
            Path("/root"),
            shared_dir,
            ignore=lambda src, names: ignore_list,
            ignore_dangling_symlinks=True,
            dirs_exist_ok=True,
        )

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('min_mapq', min_mapq),
                *get_flag('aligner', aligner),
                *get_flag('r1_bc_pattern', r1_bc_pattern),
                *get_flag('r2_bc_pattern', r2_bc_pattern),
                *get_flag('r1_crop', r1_crop),
                *get_flag('split_fastq_by_size', split_fastq_by_size),
                *get_flag('split_fastq_by_part', split_fastq_by_part),
                *get_flag('datatype', datatype),
                *get_flag('input', input),
                *get_flag('outdir', outdir),
                *get_flag('genome', genome),
                *get_flag('fasta', fasta),
                *get_flag('gtf', gtf),
                *get_flag('regions_mask', regions_mask),
                *get_flag('additional_fasta', additional_fasta),
                *get_flag('multiqc_methods_description', multiqc_methods_description)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_callingcards", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_callingcards(r1_bc_pattern: typing.Optional[str], r2_bc_pattern: typing.Optional[str], r1_crop: typing.Optional[int], split_fastq_by_size: typing.Optional[int], datatype: str, input: LatchFile, outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], genome: typing.Optional[str], fasta: typing.Optional[LatchFile], gtf: typing.Optional[str], regions_mask: typing.Optional[LatchFile], additional_fasta: typing.Optional[LatchFile], multiqc_methods_description: typing.Optional[str], min_mapq: typing.Optional[int] = 10, aligner: typing.Optional[str] = 'bwamem2', split_fastq_by_part: typing.Optional[int] = 10) -> None:
    """
    nf-core/callingcards

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, min_mapq=min_mapq, aligner=aligner, r1_bc_pattern=r1_bc_pattern, r2_bc_pattern=r2_bc_pattern, r1_crop=r1_crop, split_fastq_by_size=split_fastq_by_size, split_fastq_by_part=split_fastq_by_part, datatype=datatype, input=input, outdir=outdir, genome=genome, fasta=fasta, gtf=gtf, regions_mask=regions_mask, additional_fasta=additional_fasta, multiqc_methods_description=multiqc_methods_description)

