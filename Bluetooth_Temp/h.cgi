#!/usr/bin/perl
use DBI;

my $database='yfhome';
my $server  ='yfhomeserver.local';
my $username='www';
my $password='www';

my $dsn = "DBI:mysql:database=$database:host=$server";
my $dbh = DBI->connect($dsn, $username, $password) || die "Can't connect.\n";

my $dsid = "";
my @locs = ("Up Room", "Up Out 18", "Fish Zero", "Down Room Zero");
my $k = 1;
my $procid = $$;

my $day3 = time - 4*86400;

# for CGI header
$|=1;

print "Content-type: image/png\n\n";

foreach $loc (@locs) {

    $sql = qq[ SELECT id from ds18b20 where location = "$loc" ];

    $sth = $dbh->prepare($sql) || die "DBI error with connect to database.\n";
    $result = $sth->execute  || die "DBI error with execute.\n";

    if ($sth->rows) {
	@row = $sth->fetchrow;
	$dsid = $row[0];
    } 

    $sth->finish;

    next if $dsid == "";

    $sql = qq[ SELECT DATE_FORMAT(from_unixtime(time), '%m/%e %T') AS mtime, 
               temperature FROM home_temp WHERE location = "$dsid" AND time > $day3 ];
    
    $sth    = $dbh->prepare($sql) || die "DBI error with connect to database.\n";
    $result = $sth->execute       || die "DBI error with execute.\n";

    $tmpfile = "/tmp/tmpdata$procid$k.dat";
    open(OUTPUT, ">$tmpfile") || die ("Can't write data file");
    if ($sth->rows) {
	$nums = $sth->{'NUM_OF_FIELDS'};
	while (@row = $sth->fetchrow) {
	    for ($i=0; $i< $nums ; $i++ ) {
		print OUTPUT "$row[$i]\t";
	    }
	    print OUTPUT "\n";
	}
    }
    $sth->finish;
    close(OUTPUT);
    $k++;
} #foreach

$imgfile = "/tmp/tmp$procid.png";
$gnuplot = "|/usr/bin/gnuplot";

$gplot = qq[ set term pngcairo enhanced size 2048,1536
             set output  "$imgfile"
	     set title   "96小时以来的室温"
	     set xlabel  "日期 时间"
	     set timefmt "%m/%d %H:%M:%S"
	     set xdata   time
	     set ylabel  "摄氏度 {/Symbol \260}C"
	     set grid
	     array titles[4] = ["阁楼", "户外", "鱼缸", "客厅"]
             plot for [i=1:$k-1] file="/tmp/tmpdata$procid".i.".dat" file using 1:3 t titles[i] w line lw i
     ];

# use GNUPLOT to draw the figure
open(GNUPLOT, $gnuplot);
print GNUPLOT $gplot;
close(GNUPLOT);

do { 
    $tmpfile = "/tmp/tmpdata$procid$k.dat";
    unlink($tmpfile);
} while ($k-- > 0) ;

# send the image data to client
open(INPUT, "<$imgfile");
while(<INPUT>) {
	print;
}
close(INPUT);
unlink($imgfile);

$dbh->disconnect;
