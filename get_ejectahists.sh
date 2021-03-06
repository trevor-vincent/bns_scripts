if [ ! $# -eq 2 ]; then
    echo "get_ejectahists.sh <Lev0_XX> <THETA_MAX>"
    exit
fi

LEV=$1
THETA=$2

if [ ! -f "ParticlesFromOutFlowCat.dat" ]; then
    echo "Can't find ParticlesFromOutFlowCat.dat, will create now"
    concat_particlesoutflow.sh $LEV
fi

echo "Copying MatterObserver files "
cp "${PWD}/${1}/Run/MatterObservers/VinfBin.agr" .
cp "${PWD}/${1}/Run/MatterObservers/YeBin.agr" .

echo "Running ejecta_vinf_hist ... "
ejecta_vinf_hist_ext.py "left_grid_only" "all" -1
ejecta_vinf_hist_ext.py "on_grid_only" "all" -1
ejecta_vinf_hist_ext.py "combined" "all" -1
ejecta_vinf_hist_ext.py "left_grid_only" "polar" $THETA
ejecta_vinf_hist_ext.py "left_grid_only" "equatorial" $THETA

echo "Running ejecta_ye_hist ... "
ejecta_ye_hist_ext.py "left_grid_only" "all" -1
ejecta_ye_hist_ext.py "on_grid_only" "all" -1
ejecta_ye_hist_ext.py "combined" "all" -1
ejecta_ye_hist_ext.py "left_grid_only" "polar" $THETA
ejecta_ye_hist_ext.py "left_grid_only" "equatorial" $THETA

#echo "Copying DataForMovies files "
#cp "${PWD}/${1}/Run/DataForMovies/"*.dat .

#echo "Creating rhocontour "
#make_movie_ye_rhocontour_with_line.py Ye_vert.dat Rho0Phys_vert.dat UnboundFlagH_vert.dat xz $THETA
