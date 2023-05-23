#!/usr/bin/env nextflow
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nf-core/callingcards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Github : https://github.com/nf-core/callingcards

    Website: https://nf-co.re/callingcards
    Slack  : https://nfcore.slack.com/channels/callingcards
----------------------------------------------------------------------------------------
*/

nextflow.enable.dsl = 2

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GENOME PARAMETER VALUES
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
params.fasta = WorkflowMain.getGenomeAttribute(params, 'fasta')
params.gtf = WorkflowMain.getGenomeAttribute(params, 'gtf')

if (params.datatype == 'yeast'){
    if(params.genome == 'R64-1-1'){

        params.regions_mask = "${projectDir}/assets/yeast/igenomes/R64-1-1/regions_mask.bed"
        log.info"Using default regions mask for yeast analysis: ${params.regions_mask}"

        params.fasta_index = null
        log.info"Genome fasta will be indexed in the workflow"
    }
    if(!params.containsKey('additional_fasta')){
        params.additional_fasta = "${projectDir}/assets/yeast/plasmid_sequences.fasta"
        log.info"Using default plasmid sequences for yeast analysis: ${params.additional_fasta}"
    }
}

if (params.genome == 'GRCm38'){
    if(params.aligner == 'bwa'){
        params.bwa_index = WorkflowMain.getGenomeAttribute(params, 'bwa')
    }
}

if (params.genome == 'GRCh38'){
    if(params.aligner == 'bwa'){
        params.bwa_index = WorkflowMain.getGenomeAttribute(params, 'bwa')
    }
}

if(!params.containsKey('regions_mask')){
    params.regions_mask = null
    log.info"Regions mask not specified. The entire genome will be used for alignment"
}

if(!params.containsKey('additional_fasta')){
    params.additional_fasta = null
    log.info"Additional fasta not specified. No additional sequences beyond those in the genome fasta will be used for alignment"
}

if (!params.containsKey('fasta_index')){
    params.fasta_index = null
    log.info"Genome fasta will be indexed in the workflow"
}

// these parameters are used in the pipeline and may or may not be set either
// by the user or through the --genome argument. If they are null, then
// the appropriate index will be created in the workflow
if(!params.containsKey('bwa_index')){
    params.bwa_index = null
}
if(!params.containsKey('bwamem2_index')){
    params.bwamem2_index = null
}
if(!params.containsKey('bowtie_index')){
    params.bowtie_index = null
}
if(!params.containsKey('bowtie2_index')){
    params.bowtie2_index = null
}
/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    VALIDATE & PRINT PARAMETER SUMMARY
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

WorkflowMain.initialise(workflow, params, log)

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    NAMED WORKFLOW FOR PIPELINE
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

include { CALLINGCARDS_MAMMALS } from './workflows/callingcards_mammals'
include { CALLINGCARDS_YEAST   } from './workflows/callingcards_yeast'

//
// WORKFLOW: Run main nf-core/callingcards analysis pipeline
//
workflow NFCORE_CALLINGCARDS_MAMMALS {
    CALLINGCARDS_MAMMALS ()
}

workflow NFCORE_CALLINGCARDS_YEAST {
    CALLINGCARDS_YEAST ()
}

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    RUN ALL WORKFLOWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/

//
// WORKFLOW: Execute a single named workflow for the pipeline
// See: https://github.com/nf-core/rnaseq/issues/619
//
workflow {
    if(params.datatype == 'mammal'){
        NFCORE_CALLINGCARDS_MAMMALS ()
    } else if (params.datatype == 'yeast'){
        NFCORE_CALLINGCARDS_YEAST ()
    } else {
        exit 1, "Invalid datatype specified: ${params.datatype}. " +
        "Valid options are 'mammals' or 'yeast'"
    }

}

/*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    THE END
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*/
