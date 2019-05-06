# Contributing to the EMPD

:+1::tada: Thank you! The EMPD is a community based database - so we rely on your contributions!! :tada::+1:

The following set of guidelines for contributing to the EMPD are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.
#### Table Of Contents

[Code of Conduct](#code-of-conduct)

[How Can I Contribute?](#how-can-i-contribute)
  * [Quick and Dirty](#quick-and-dirty)
  * [Through Github](#through-github)
    * [Reporting Bugs](#reporting-bugs)
    * [Suggesting Changes](#suggesting-enhancements-through-github)
    * [Contributing new data](#contributing-new-data-through-github)

## Code of Conduct

This project and everyone participating in it is governed by the [EMPD Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Quick and Dirty
If you just want to report an error without going through our guidelines, you do not need a Github account. Just click [here](https://empd2.github.io/?tab=report-issue) and fill out the form.

If you want to contribute new data, you can download and fill out the [Excel template](https://github.com/EMPD2/EMPD-data/blob/master/templates/EMPD_Metadata_Template-2.xls?raw=true).  You should complete this as best you can and submit it together with your pollen data files to basil.davis@unil.ch. It would be a great help.

### Through Github

#### Reporting Bugs

This section guides you through submitting a bug report for the EMPD. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please check existing [issues](https://github.com/EMPD2/EMPD-data/issues) and [pull requests](https://github.com/EMPD2/EMPD-data/pulls) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

##### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/). You can either report an issue through the EMPD2 viewer at [EMP2.github.io](https://empd2.github.io/?tab=report-issue), or, if you have an account on Github, you can create an issue on the EMPD-data repository.

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **If you have additional publications**, etc. that support the issue you are reporting, please provide their DOI.
* **If you want to change the meta data of a sample** you can also make contribute through a pull request (see [Suggesting Changes](#suggesting-enhancements)). But you can also leave this to the maintainers, just make sure to provide all necessary information to fulfill you request.

#### Suggesting Changes

If you want to change an existing sample and have an account on Github (alternatively, see the [quick and dirty](#quick-and-dirty) instructions), 

1. [fork the EMPD-data repository](https://github.com/EMPD2/EMPD-data/fork)
2. copy the [templates/empty.tsv](templates/empty.tsv) file to the root of your repository (i.e. into the folder of the `meta.tsv`file).
3. With the line from [meta.tsv](https://github.com/EMPD2/EMPD-data/blob/master/meta.tsv) for the sample(s) you want to change.
4. Change or add the missing information in the corresponding lines of the newly created document.

> **Note:** You can also open and edit this file in Microsoft Excel. After step 2, just open Excel, click File ▶ Open and navigate to the copy of `empty.tsv`.

#### Contributing new data through Github

We very much welcome contributions through pull requests on Github (if you have a Github account and are familiar with it, alternatively, see the [quick and dirty](#quick-and-dirty) instructions). To contribute new samples, 

1. [fork the EMPD-data repository](https://github.com/EMPD2/EMPD-data/fork)
2. Download the [Excel template](https://github.com/EMPD2/EMPD-data/blob/master/templates/EMPD_Metadata_Template-2.xls?raw=true) and fill out the `EMPD_Metadata` sheet. You can add one sample per row in this file.
3. Save the `EMPD_Metadata` sheet as tab-delimited text. Do this via File ▶ Save As... and then select `Tab delimited Text (.txt)` from the *File Format* dropdown menu.
4. Now to the pollen data: 
   i. For each sample that you want to contribute, copy the [templates/pollen_data.tsv](templates/pollen_data) to the [samples](samples) directory.
   ii. Now rename the copy to `SampleName.tsv`, where `SampleName` should be replaced by the name you use in the `SampleName` column of your meta data. Fill this file with the tab-delimited data of your sample, one line per taxon (see [samples/Atanassova_a1.tsv](samples/Atanassova_a1.tsv) for example). Don't worry with the `acc_varname`, we can sort this out later.
5. Commit your new files and push them to your fork. Then create a pull request into the master branch of the EMPD and the core-maintainers will review it.
