./run.py 80m_converge --directory ./Configs/80m_tbf/ \
    --show  \
    --build \
    --rerun \
    --time 60
./run.py 80m_single -d ./Configs/80m_one_tbf/ --show no --build yep

./run.py 80m_single_bbr1 --directory ./Configs/80m_one_bbr1 --show --time 60 --parse --rerun