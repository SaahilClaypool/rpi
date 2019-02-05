for x in `fd summary.csv -I`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

# individual trials I care about

FOLDER=./80_BBR_4/Trial_2000000_2/
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

FOLDER=./80_BBR_vs_Cubic_4/Trial_125000_2/
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

FOLDER=./80_BBR_vs_Cubic_4/Trial_437500_2/
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done


FOLDER=./80_BBR_vs_Cubic_4/Trial_2000000_2
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

# individual trials I care about

FOLDER=./80_BBR_4/Trial_2000000_2/
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

FOLDER=./80_BBR_4/Trial_125000_2
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

FOLDER=./80_BBR_4/Trial_437500_2/
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

FOLDER=./80_BBR_4/Trial_2000000_2
for x in `fd csv -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done
for x in `fd start_time.txt -I $FOLDER`;
    do rsync -vR $x ~/raspberry/bbr-nossdav-19/Graphs/Data
done

