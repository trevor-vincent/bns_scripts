for d in $(ls -d */); do
cd $d
echo $d
if [ -f "./points.log" ] 
then
echo "found points.log"
/scinet/niagara/software/2018a/opt/base/anaconda3/5.1.0/bin/python3 /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/d4est_plot_points.py
#python3 /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/d4est_plot_points.py "${PWD}/points.log"
fi
if [ -f "./iterations.log" ] 
then
echo "found iterations.log"
/scinet/niagara/software/2018a/opt/base/anaconda3/5.1.0/bin/python3 /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/d4est_plot_its.py
#python3 /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/d4est_plot_its.py "${PWD}/iterations.log"
fi
cd ..
done

