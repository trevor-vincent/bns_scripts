find . -name "DensestPoint.dat" | sort -k2 > folders.txt

linenum=$(cat -n folders.txt | grep $1 | cut -d '.' -f1)
head folders.txt -n $linenum > folders_cropped_rho0_xy.txt

emacs -nw folders_cropped_rho0_xy.txt &&

read -p "Continue (y/n)?" choice
case "$choice" in
    y|Y ) echo "yes";;
    n|N ) echo "no" && exit;;
    * ) echo "invalid";;
esac

cat $(cat folders_cropped_rho0_xy.txt) > densest_point_total.dat
