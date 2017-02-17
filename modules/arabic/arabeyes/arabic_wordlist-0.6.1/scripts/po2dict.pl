#!/usr/bin/perl
# -*-Perl-*-

#---
# $Id: po2dict.pl,v 1.4 2004/03/13 02:02:25 nadim Exp $
#
# ------------
# Description:
# ------------
#  This script will read all 26 full_wordlist_*.po files and generate
#  a dict compliant English/Arabic dictionary & index files to be used
#  via dictd.
#
#  You will need to restart dictd after adding the above 2 files
#  (namely the dictionary and index file) to your dictionary directory
#  so you can have access to them and see them.
#
#  This script is meant to run in the same directory as your .po files.
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2004/03/13 02:02:25 $
#  $Author: nadim $
#  $Revision: 1.4 $
#  $Source: /home/arabeyes/cvs/translate/wordlist/scripts/po2dict.pl,v $
#
# (www.arabeyes.org - under GPL license)
#---

require "newgetopt.pl";

##
# Specify global variable values and init some Variables
$this_script	= $0;
$this_script    =~ s|^.*/([^/]*)|$1|;

# Modify the following line if you need to and leave the rest intact
# This is the default dictionary directory under Debian. Please note
# You need to be 'root' in order to copy the dictionary & index files
# to the default location.
$dict_dir	= "/usr/share/dictd";

# Make sure the directory exists
if (!-d $dict_dir)
{
   die "<<!>> ERROR($this_script): please create '$dict_dir' \n";
}

# Process the command line
&get_args();

# Make sure we have a bonafide ready-to-append-to dirname
if ($opt_dir)
{
    if ($opt_dir !~ /\/$/)
    {
	$opt_dir = "$opt_dir/";
    }
}

# Background info gathering
chop($date  = `date`);
chop($year  = `date +%Y`);
chop($month = `date +%m`);

# Some constants
$webfiles	= "www.arabeyes.org";
$dictname	= "Arabeyes English/Arabic dictionary";
$out_file	= "dictd.input";
$dictfmt	= "dictfmt -j -u \"$webfiles\" -s \"$dictname\" arabic";
$dictd_restart	= "/etc/init.d/dictd restart";
$dictd_log	= "/home/arabeyes/logs/dictd/log.$year$month";

# The following loop reads all 26 files and generates a text
# file that is suitable as an input for dictfmt to generate
# the dictionary & index files
foreach $letter ('A'..'Z')
{
    $dest = $opt_dir . "full_wordlist_" . $letter . ".po";
    open (IN, "< $dest") or
	die "<<!>> ERROR($this_script): Can't open file $dest for reading: $!";
    while (<IN>)
    {
	if (/^msgid\s+"(.*)"/)  { push(@out, ":$1: "); $num_terms++; }

	if (/^msgstr\s+"(.*)"/) { push(@out, "$1\n");  }
    }
    close(IN);
}

# Dump out the generated file (ie. the input to dictfmt)
open (OUT, "> $out_file") or
    die "<<!>> ERROR($this_script): Can't open file $out_file for writing: $!";

# Include whatever info should be noted in the 'info' header
print OUT qq
|=== =============================================================== ===
This dictionary file is under GNU's GPL license.
For more info, please inspect thoroughly the following link,

   http://www.gnu.org/licenses/gpl.html

If you'd like to help, please visit,

  http://www.arabeyes.org/project.php?proj=Wordlist
  http://www.arabeyes.org/project.php?proj=QaMoose

NOTE: This file contains $num_terms terms.
|;

# Dump out the actual lines collected from before
foreach $line (@out) { print OUT $line; }

close(OUT);

# Generate dictd compliant dictionary & index file
(!system("$dictfmt < $out_file")) or
    die "<<!>> ERROR($this_script): Failed to run dictfmt: $!";

# Move resulting dictionary & index files to dictionary directory
rename("arabic.dict", "$dict_dir/arabic.dict") or
    die "<<!>> ERROR($this_script): Failed copy arabic.dict to $dict_dir: $!";

rename("arabic.index", "$dict_dir/arabic.index") or
    die "<<!>> ERROR($this_script): Failed copy arabic.index to $dict_dir: $!";

# Accumulate all log info (and restarts) in a single file
# - in association with /etc/init.d/dictd of course
$logfile_existed = (-e $dictd_log);

# With files moved, restart the dictd daemon to apply the changes
(!system("$dictd_restart")) or
    die "<<!>> ERROR($this_script): Failed to restart dictd: $!";

open (LOG, ">> $dictd_log") or
    die "<<!>> ERROR($this_script): Can't open log $dictd_log: $!";
print LOG "--- RESTARTED ($date) ---\n";
close(LOG);

# Make sure file is owned by the right entity (if its newly created)
if ( !$logfile_existed )
{
    chown ( ((getpwnam(dictd))[2]), ((getpwnam(dictd))[3]), $dictd_log );
}

# Do some minor cleaning-up
unlink("$out_file");

# Normal exit
exit(0);

       ###        ###
######## Procedures ########
       ###        ###

##
# Get the command line arguments
sub get_args
{
  &NGetOpt (
            "dir=s",		# Specify the starting dir of the tree
           ) || ( $? = 257, die "Invalid argument\n" );
}
