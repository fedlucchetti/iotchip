# Contributing to Eden

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to Eden IoT Chip project, which is developed by [Eden Synthetics](https://gitlab.com/edensynth) on GitLab.
These are just guidelines, not rules, use your best judgment and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Code of Conduct](#code-of-conduct)
  * [IoT Chip Packages](#iot-chip-packages)
  * [Eden Design Decisions](#design-decisions)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Specs Styleguide](#specs-styleguide)
  * [Documentation Styleguide](#documentation-styleguide)

[Using As Runnable](#using-as-runnable)
  * [Cloning To A Chip](#cloning-to-a-chip)

## What should I know before I get started?

### Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [es@edensynth.com](mailto:es@edensynth.com).

### IoT Chip Packages

Eden IoT Chip Project is a large closed-source partially open source project—it's made up of over [100 repositories](https://gitlab.com/edensynth/iotchip).
When you initially consider contributing to Eden Synthetics IoT Chip Project, you might be unsure about which of those 100 repositories implements the functionality you want to change or report a bug for.
This section should help you with that.

The main languages and technologies involved in this project are:

* Shell/Bash scripting
* C
* Python
* Javascript
* PHP
* HTML/CSS

Eden is intentionally very modular.
Nearly every element you interact with comes from a package or a class, even fundamental things like Microchip and the Webcam.

Continue from https://github.com/atom/atom/blob/master/CONTRIBUTING.md