source venv/bin/activate
export PYTHONPATH=$(pwd)

which python


for YEAR in 2018 2019 2020 2021 2022 2023
do
    for MONTH in 1 2 3 4 5 6 7 8 9 10 11 12
    do
        python arxiv_scrapper/scrapper_search.py $YEAR $MONTH
    done
done
