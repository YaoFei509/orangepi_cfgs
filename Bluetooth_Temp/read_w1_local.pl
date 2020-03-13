#!/usr/bin/perl

#scan all DS18B20s
$sensors = `ls /sys/bus/w1/devices`;
@sen = split /\s/, $sensors;

foreach $s (@sen) {
    next if ($s !~/^28/) ; #only read DS18B20
    
    $sensor_temp = `cat /sys/bus/w1/devices/$s/w1_slave 2>&1`; 
    if ($sensor_temp !~/No such file or directory/) { 
	if ($sensor_temp !~/NO/) { 
	    $s =~ s/28-(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)(\w\w)/28:$1:$2:$3:$4:$5:$6/;
	    $sensor_temp =~ /t=(\d+)/i; 
	    
	    $st = $1/1000; 
	    print "mac = $s  temp = $st\n";
	}
    }
}
