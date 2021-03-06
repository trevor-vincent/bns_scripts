#NeutrinoFluxaAtBoundary.dat
#NeutrinoFluxeAtBoundary.dat
#NeutrinoFluxxAtBoundary.dat

/scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/rename_oldneutrinofiles.sh

find . -name "NeutrinoFluxaAtBoundary.dat" | sort -k2 > folders.txt

linenum=$(cat -n folders.txt | grep $1 | cut -d '.' -f1)
head folders.txt -n $linenum > folders_cropped_rho0_xy.txt

emacs -nw folders_cropped_rho0_xy.txt &&

read -p "Continue (y/n)?" choice
case "$choice" in
    y|Y ) echo "yes";;
    n|N ) echo "no" && exit;;
    * ) echo "invalid";;
esac

cat $(cat folders_cropped_rho0_xy.txt) > neutrinofluxa_total.dat

sed -i 's/NeutrinoFluxaAtBoundary.dat/NeutrinoFluxeAtBoundary.dat/g' folders_cropped_rho0_xy.txt

cat $(cat folders_cropped_rho0_xy.txt) > neutrinofluxe_total.dat

sed -i 's/NeutrinoFluxeAtBoundary.dat/NeutrinoFluxxAtBoundary.dat/g' folders_cropped_rho0_xy.txt

cat $(cat folders_cropped_rho0_xy.txt) > neutrinofluxx_total.dat

rm -f folders*.txt
