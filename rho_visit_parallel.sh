function submit_niagara_no_vtk {
cat <<EOF > submit_niagara.sh
#!/bin/bash
#SBATCH --nodes=$1
#SBATCH --time=0-$2:00           # time (DD-HH:MM)

SPEC_HOME='/scratch/p/pfeiffer/tvincent/SpEC_NOLEAK'
source $SPEC_HOME/MakefileRules/this_machine.env
                                                      
EOF
}

function submit_niagara {
cat <<EOF > submit_niagara.sh
 #!/bin/bash
#SBATCH --nodes=$1
#SBATCH --time=0-$2:00           # time (DD-HH:MM)

SPEC_HOME='/scratch/p/pfeiffer/tvincent/SpEC_NOLEAK'
source $SPEC_HOME/MakefileRules/this_machine.env

cd $3
mpirun -np $4 --map-by node ApplyObservers -t Rho0Phys,Rho,Temp,Ye -r Scalar,Scalar,Scalar,Scalar -d 3,3,3,3 -s=1 -domaininput ../../HyDomain.input -o 'ConvertToVtk(Input=Rho0Phys,Rho,Temp,Ye;Basename=Rho)' -NoDomainHistory -TimeParallel
                                                      
EOF
}

if [ "$#" -ne 4 ]; then
    echo "get_rho_parallel_visit.sh <nodes> <hours> <total_cores> <get_pvd_first>"
    exit
fi

if [ "$4" == "1" ]; then
    echo "getting vtk files first"
    submit_niagara $1 $2 $PWD $3
else
    echo "skipping vtk file generation"
    submit_niagara_no_vtk $1 $2 $PWD $3
fi

cat /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/rho_visit_parallel_aux.txt >> submit_niagara.sh
sed -i "s/REPLACE_ME_HERE/$3/g" submit_niagara.sh


# CURRENT=$PWD
# for d in $(ls -d */ | grep TimeParallel); 
# do
# echo "Starting $d"; 
# cd $CURRENT/$d
# Mtime=$(cat Rho.pvd | grep timestep | head -n1 | cut -d '=' -f2 | cut -d ' ' -f1 | sed 's/"//g')
# cd $CURRENT
# echo "module load visit && visit -cli -nowin -s /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Scripts/rho_visit_with_args.py $CURRENT/$d/Rho.visit rho_$Mtime" >> commands.txt
# done

#cd /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Evolutions/nsns_id_dd2_m1.2_m1.56_eccred0_eccred1/Ev/Lev0_AB-Merger/Lev0_BO/Run_noneutrion_m1regrid/HyVolumeData
#mpirun -np 24 --map-by node ApplyObservers -t Rho0Phys,Rho,Temp,Ye,Pressure,Enth -r Scalar,Scalar,Scalar,Scalar,Scalar,Scalar -d 3,3,3,3,3,3 -s=1 -domaininput ../../HyDomain.input -o 'ConvertToVtk(Input=Rho0Phys,Rho,Temp,Ye,Pressure,Enth;Basename=Rho)' -NoDomainHistory -TimeParallel

#visit -cli -nowin -s rho_visit.py
#cat Rho.pvd | grep timestep | head -n1 | cut -d '=' -f2 | cut -d ' ' -f1 | sed 's/"//g'

#module load visit && visit -cli -nowin -s rho_visit_with_args.py /scratch/p/pfeiffer/tvincent/BNS_Disks_project/Evolutions/nsns_id_dd2_m1.2_m1.56_eccred0_eccred1/Ev/Lev0_AB-Merger/OLDER_RUNS/Lev0_BO/606572/HyVolumeData/TimeParallelFolder0/Rho.visit testtrumpy

#scontrol show hostname ${SLURM_JOB_NODELIST} > ./node_list_${SLURM_JOB_ID}
#parallel --jobs 40 --sshloginfile ./node_list_${SLURM_JOB_ID} :::: commands.txt





