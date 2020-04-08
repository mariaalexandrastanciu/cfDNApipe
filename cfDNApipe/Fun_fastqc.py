# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 18:27:32 2019

@author: zhang
"""

from .StepBase import StepBase
from .cfDNA_utils import flatten
import os
from .Configure import Configure

__metaclass__ = type


class fastqc(StepBase):
    def __init__(self,
                 fastqInput=None,
                 fastqcOutputDir=None,
                 threads=1,
                 other_params=None,
                 stepNum=None,
                 upstream=None,
                 **kwargs):
        """
        This function is used for fastq file quality control.
        Note: this function is calling FASTQC.

        fastqc(fastqInput=None, fastqcOutputDir=None, threads=1, other_params=None, stepNum=None, upstream=None)
        {P}arameters:
            fastqInput: list, fastq files.
            fastqcOutputDir: str, output result folder, None means the same folder as input files.
            threads: int, how many thread to use.
            other_params: dict, other parameters passing to FASTQC.
                          "-parameter": True means "-parameter" in command line.
                          "-parameter": 1 means "-parameter 1" in command line.
            stepNum: int, step number for folder name.
            upstream: upstream output results, used for pipeline.
        """

        super(fastqc, self).__init__(stepNum, upstream)
        if upstream is None:
            self.setInput("fastqInputs", fastqInput)
            self.checkInputFilePath()
            if fastqcOutputDir is None:
                self.setOutput(
                    "outputdir",
                    os.path.dirname(
                        os.path.abspath(self.getInput("fastqInputs")[0])),
                )
            else:
                self.setOutput("outputdir", fastqcOutputDir)

            self.setParam("threads", threads)

        else:
            # check Configure for running pipeline
            Configure.configureCheck()
            upstream.checkFilePath()

            self.setParam("type", Configure.getType())

            self.setInput(
                "fastqInputs",
                list(
                    flatten(
                        [upstream.getOutput("fq1"),
                         upstream.getOutput("fq2")])),
            )
            self.checkInputFilePath()

            self.setOutput("outputdir", self.getStepFolderPath())

            self.setParam("threads", Configure.getThreads())

        if other_params is None:
            self.setParam("other_params", "")
        else:
            self.setParam("other_params", other_params)

        # create cmd
        cmd = self.cmdCreate([
            "fastqc",
            "--outdir",
            self.getOutput("outputdir"),
            "--threads",
            self.getParam("threads"),
            self.getParam("other_params"),
            self.inputs["fastqInputs"],
        ])

        finishFlag = self.stepInit(upstream)

        if not finishFlag:
            self.run(cmd)

        self.stepInfoRec(cmds=[cmd], finishFlag=finishFlag)
