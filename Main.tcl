#UNIT: kN m t kPa s
wipe

puts "System"
model basic -ndm 3 -ndf 6

puts "Node"
source Node.tcl

puts "Mass"
source Mass.tcl

puts "Restraint"
source Body.tcl
source Fix.tcl

puts "Material"
source Material.tcl

puts "Section"
source Section.tcl

puts "Transformation"
source Geomtransf.tcl

puts "Element"
puts "Bearing"
source Element.tcl

puts "Gravity"
source Gravity.tcl

puts "analysis"
#Gravity Analysis
#----------------------------------
constraints Transformation
numberer Plain
system BandGeneral
test NormDispIncr 1.0e-6 6
algorithm Newton
integrator LoadControl 0.1
analysis Static
analyze 10
#----------------------------------

#Modal Analysis
#----------------------------------
set mode [open mode.out w]
puts  $mode "    Period               Frequency"
puts  $mode "    T/sec                f/Hz" 
set eigenvalue [eigen 10]
for {set i 0} {$i<10} {incr i 1} {
    set lambda    [lindex $eigenvalue $i]
    set omega     [expr pow($lambda,0.5)]
    set Period    [expr 2*3.14/$omega]
    set Frequency [expr 1/$Period]
    # period (sec.) and frequency 
    puts $mode "$Period\t       $Frequency"
}
close $mode

puts "mode analysis finished!"
puts $details "mode analysis finished!"
puts "---------------------"
puts $details "---------------------"	