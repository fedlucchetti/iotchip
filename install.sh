#!/bin/bash
# clear

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export installdir="$DIR"
export setupdir="setup"
export rundir="run"
cd "$installdir/$setupdir"

chmod +x "$installdir/$setupdir/install.sh"
"$installdir/$setupdir/install.sh"
