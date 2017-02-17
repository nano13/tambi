#!/usr/bin/perl
# -*-Perl-*-

#---
# $Id: wordlist_add.pl,v 1.9 2003/10/14 01:50:32 nadim Exp $
#
# ------------
# Description:
# ------------
#  This script will read an input specified file which includes new
#  terms (either single non-translated term/word per line or a newly
#  translated .po file) and will check for the new term's existence
#  in the various full_wordlist_* files (ie. NO duplicates) - if they
#  are there already, nothing is done otherwise the new terms are
#  sorted and added in the right location in the right file.
#
#  This script is NOT the most elegant way to do this and does not
#  serve as a good learning opportunity for those seeking more Perl
#  knowledge (too many global variables, etc).  Since this script
#  will NOT be run often its deemed sufficient to do the job at hand.
#
# -----------------
# Revision Details:    (Updated by Revision Control System)
# -----------------
#  $Date: 2003/10/14 01:50:32 $
#  $Author: nadim $
#  $Revision: 1.9 $
#  $Source: /home/arabeyes/cvs/translate/wordlist/scripts/wordlist_add.pl,v $
#
#---

require "ctime.pl";
require "newgetopt.pl";

use English;

##
# Keep track of run-time
$glb_start_time	= time;

##
# Specify global variable values and init some Variables
$in_script	= $0;
$in_script	=~ s|^.*/([^/]*)|$1|;

##
# Find how many spaces the scripts name takes up (nicety)
$in_spaces	= $in_script;
$in_spaces	=~ s/\S/ /g;

##
# Process the command line
&get_args();

if ( $opt_help ) { &help; }

if (!$opt_new_file) { &usage(1); }

print "<< * >> Using $in_script\n";

##
# Specify all the valid letters
foreach my $let ('A'..'Z')
{
    $letters_ok{$let} = 1;
}

# Read the new terms file
&readin_new();

if ($num_empty)
{
    printf " < - > Skipped   %5u empty terms \n", $num_empty;
}

# Cycle through all the letters we've been presented and produce output
#foreach $letter ('A'..'Z')
foreach my $letter (sort (keys %letters_do))
{
    $num_new = 0;
    undef @output;

    &readin_master($letter);
    &check_terms($letter);

    printf " < - > Processed %5u new terms for letter - $letter \n", $num_new;
    $tot_num_new += $num_new;
}

printf " < + > Totals  - %5u NEW, %5u OLD, %5u SKIP  => %5u Total\n",
    $tot_num_new, $num_old, $num_empty, $num_total;

# Tell 'em how long the whole we were ON
&report_run_time($glb_start_time);

exit(0);

       ###        ###
######## Procedures ########
       ###        ###

##
# Read-in the new terms file
sub readin_new
{
    open (NEW, "< $opt_new_file") or
	die "<<!>> ERROR($in_script): Can't open $opt_new_file - $!";
    while (<NEW>)
    {
	chomp;

	# Check if we are adding new translated words or just Raw list
	if ($opt_new_file =~ /\.po/)
	{
	    # - Dealing with a translated file
	    if (/^msgid\s+\"(\S+.*)\"/)
	    {
		if (defined $term_msgid)
		{
		    my $msg = "Malformed msgid's - (back-to-back) ?";
		    die "<<!>> ERROR($in_script): $msg \n";
		}
		my $term_cap	= ucfirst($1);
		my $out_msgid	= "msgid \"$term_cap\"";
		$term_msgid	= uc($1);
		$assoc_new{$term_msgid}	= $1;
		$assoc_new{$term_msgid}{'translated'}{'msgid'} = $out_msgid;
#		$assoc_new{$term_msgid}	= { translated => {msgid => $_} };
		$num_total++;
	    }
	    if (/^msgstr\s+\"(.*)\"/ && $term_msgid)
	    {
		# See if only translated terms are sought after
		if ($opt_translated && ($1 !~ /\S+/))
		{
		    delete $assoc_new{$term_msgid};
		    undef $term_msgid;
		    $num_empty++;
		    next;
		}
		$assoc_new{$term_msgid}{'translated'}{'msgstr'} = $_;

		# Get first letter of word and enable its processing
		my $f_letter	= uc(substr($term_msgid, 0, 1));
		if ($letters_ok{$f_letter}) { $letters_do{$f_letter} = 1; }
		undef $term_msgid;
	    }
	}
	else
	{
	    # - Dealing with Raw list
	    # Capitalize
	    $assoc_new{uc($_)}	= ucfirst($_);
	    my $f_letter	= uc(substr($_, 0, 1));
	    if ($letters_ok{$f_letter}) { $letters_do{$f_letter} = 1; }
	    $num_total++;
	}
    }
    printf " < + > Read      %5u new terms for processing\n", $num_total;
    close (NEW);
}

##
# Read-in the original master file
sub readin_master
{
    my ($r_letter)	= @_;

    $filename		= "full_wordlist_$r_letter";
    $filename_full	= "$filename.po";

    open (ORIG_FILE, "< $filename_full") or
	die "<<!>> ERROR($in_script): Can't open $filename_full - $!";
    while (<ORIG_FILE>)
    {
	if (/msgid\s+\"(\S+)\"/)
	{
	    # Check if word already exists
	    my $master_cap = uc($1);
	    if ($assoc_new{$master_cap})
	    {
		# If it does, invalidate it ("you're outta here")
		delete $assoc_new{$master_cap};
		$num_old++;
	    }
	}
	# Capture lines to regurgitate later
	push (@output, $_);
    }
    close (ORIG_FILE);
}

##
# Process new terms and output new results
sub check_terms
{
    my ($c_letter)	= @_;

    # Get a subsection of the letters (alphabetically)
    foreach my $key (sort (keys %assoc_new))
    {
	if ($key =~ /^$c_letter/)
	{
	    # Store off in a local assocative array (invalidate orig entry)
	    $assoc_sub{$c_letter}{$key}	= $assoc_new{$key};
	    delete $assoc_new{$key};
	    $num_new++;
	}
    }    

    # Proceed only if I have new terms
    if ($assoc_sub{$c_letter})
    {

	# If user opts for single file and file exists - augment
	# otherwise, create
	if ($opt_multi)
	{
	    $filename_multi = "${opt_multi}_$c_letter";
	}

	$out_file = $opt_single		||
	    	    $filename_multi	||
		    "$filename.new";

	if ($opt_single && -e "$out_file.po")
	{
	    $first_out = 0;
	    open (OUTF, ">> $out_file.po") or
		die "<<!>> ERROR($in_script): Can't open $out_file.po - $!";
	}
	else
	{
	    $first_out = 1;
	    open (OUTF, "> $out_file.po") or 
		die "<<!>> ERROR($in_script): Can't open $out_file.po - $!";
	}

	if ($opt_single || $opt_multi)
	{
	    &dump_out_complete($c_letter, $first_out);
	}
	else
	{
	    # Go ahead, make my day -- regurgitate
	    foreach my $line (@output)
	    {
		# Capture and hold any commented lines
		if ($line =~ /^#/)
		{
		    $commented_lines .= $line;
		    next;
		}
		if ($line =~ /msgid\s+\"(\S+)\"/)
		{
		    $orig_term = $1;
		    foreach my $key (sort (keys %{$assoc_sub{$c_letter}}))
		    {
			# Do the expected sorting
			if ($assoc_sub{$c_letter}{$key} lt $orig_term)
			{
			    &dump_out_terms($c_letter, $key);
			    delete $assoc_sub{$c_letter}{$key};
			}
		    }
		}

		# Print the output (along with any held commented lines)
		if ($commented_lines)
		{
		    print OUTF $commented_lines;
		    undef $commented_lines;
		}
		print OUTF $line;
	    }

	    # Dump out all terms that are sorted beyond last entry in file
	    foreach my $key (sort (keys %{$assoc_sub{$c_letter}}))
	    {
		&dump_out_terms($c_letter, $key);
		delete $assoc_sub{$c_letter}{$key};
	    }
	}
	close (OUTF);
    }

    # Sanity check - nothing should still be valid (all have been consumed ?)
    foreach my $key (sort (keys %{$assoc_sub{$c_letter}}))
    {
	if ($assoc_sub{$c_letter}{$key})
	{
	    print "<<!>> ERROR($in_script): $key unaccounted ($c_letter)\n";
	}
    }
}

##
# Print out a duple (a term and its associated translation or place holder)
sub dump_out_terms
{
    my ($d_letter,
	$d_key)		= @_;

    if (defined $assoc_sub{$d_letter}{$d_key}{translated})
    {
	print OUTF "$assoc_sub{$d_letter}{$d_key}{translated}{msgid}\n";
	print OUTF "$assoc_sub{$d_letter}{$d_key}{translated}{msgstr}\n\n";
    }
    else
    {
	print OUTF "#, New term - $opt_new_file\n";
	print OUTF "msgid \"$assoc_sub{$d_letter}{$d_key}\"\nmsgstr \"\"\n\n";
    }
}

##
# Print out the entire contents of a new terms
sub dump_out_complete
{
    my ($wr_letter,
	$wr_header)	= @_;

    if ($wr_header)
    {
	print OUTF qq|# Translation of $out_file.po to Arabic
#-*-
# --
# \$Id\$
# --
#
# A complete account of all English words starting with '$wr_letter'
# that need to be translated to Arabic.  This will be used
# as part of a free dictionary look-up mechanism.
#
# - Copyright (C) 2003 Free Software Foundation, Inc.
#
# To generate a simple equality list, run this command-line
#   perl -n -e 'if (/^msgid\s+"(.*)"/)  { print "$1 = "; } \
#               if (/^msgstr\s+"(.*)"/) { print "$1\\n"; }' \
#               this_file_name_here
#
#-*-
msgid ""
msgstr ""
"Project-Id-Version: $out_file\\n"
"POT-Creation-Date: 2002-08-13 18:00-0700\\n"
"PO-Revision-Date : 2002-08-23 11:15-0700\\n"
"Last-Translator: You Here <you\@email.org>\\n"
"Language-Team: Arabic <doc\@arabeyes.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"X-Generator: KBabel 1.0.1\\n"

|;
    }

    foreach my $key (sort (keys %{$assoc_sub{$wr_letter}}))
    {
	# Sanity check - terms should all be valid here
	if ($assoc_sub{$wr_letter}{$key})
	{
	    # Do the expected sorting
	    print OUTF "msgid \"$key\"\nmsgstr \"\"\n\n";
	    delete $assoc_sub{$wr_letter}{$key};
	}
    }
}
    
##
# Report the total run-time of the script
sub report_run_time
{
    my ($begin_time)    = @_;

    my (
        $end_time,
        $total_time
       );

    $end_time = time;
    $total_time = $end_time - $begin_time;
  TIME_CASE:
    {
        # Hours
        if (($total_time/3600) > 1)
        {
            printf "<< * >> Run-time = %.2f hours\n",($total_time/3600);
            last TIME_CASE;
        }
        # Minutes
        if (($total_time/60) > 1)
        {
            printf "<< * >> Run-time = %.2f minutes\n",($total_time/60);
            last TIME_CASE;
        }
        # Seconds
        print "<< * >> Run-time = $total_time seconds\n";
    }
}

##
# Print short usage info
sub usage
{
    my ($die_after) = @_;

    print qq
|Usage: $in_script <-new_file filename> [-single filename]
       $in_spaces                      [-multi  filename]
       $in_spaces                      [-translated]
       $in_spaces                      [-help]
|;

    if ( $die_after ) { exit(5); }
}

##
# Print one-liner help
sub help
{
    &usage(0);

    print qq|
-> process a new terms file to include unique new terms to full_wordlist_*

  Options:

    <-new_terms filename> : Specify filename which contains the new terms
    [-single filename]    : Dump new terms into a single file
    [-multi  filename]    : Dump new terms to multiple files (suffix _letter)
    [-translated]         : Only process translated terms
    [-help]               : Produce this help screen

|;
    exit(10);
}

##
# Get the command line arguments
sub get_args
{
  &NGetOpt (
            "help",		# print a nice help screen
            "new_file=s",	# New terms file
            "single=s",		# Don't augment - generate a single output file
            "multi=s",		# Don't augment - generate new terms only
            "translated",	# Only include translated terms
           ) || ( $? = 257, die"<<!>> ERROR($in_script): Invalid argument\n" );
}
