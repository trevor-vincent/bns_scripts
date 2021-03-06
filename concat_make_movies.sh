
find . \( -name "Rho0Phys_xy.dat" -or -name "Rho0Phys_hori.dat" \) | sort -k2 > folders.txt
cat folders.txt
linenum=$(cat -n folders.txt | grep $1 | cut -d '.' -f1)
head folders.txt -n $linenum > folders_cropped_rho0_xy.txt

emacs -nw folders_cropped_rho0_xy.txt &&

read -p "Continue (y/n)?" choice
case "$choice" in
    y|Y ) echo "yes";;
    n|N ) echo "no" && exit;;
    * ) echo "invalid";;
esac


cp folders_cropped_rho0_xy.txt folders_cropped_rho0_xz.txt
sed -i 's/_xy/_xz/g' folders_cropped_rho0_xz.txt
sed -i 's/_hori/_vert/g' folders_cropped_rho0_xz.txt
cp folders_cropped_rho0_xy.txt folders_cropped_temp_xy.txt
sed -i 's/Rho0Phys/Temp/g' folders_cropped_temp_xy.txt
cp folders_cropped_rho0_xz.txt folders_cropped_temp_xz.txt
sed -i 's/Rho0Phys/Temp/g' folders_cropped_temp_xz.txt

cat $(cat folders_cropped_rho0_xy.txt) > Rho0Phys_xy_total.dat
cat $(cat folders_cropped_rho0_xz.txt) > Rho0Phys_xz_total.dat
cat $(cat folders_cropped_temp_xy.txt) > Temp_xy_total.dat
cat $(cat folders_cropped_temp_xz.txt) > Temp_xz_total.dat
