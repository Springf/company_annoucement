from main import lambda_handler

if __name__ == "__main__":
    context = {"tickers":["vl6-koufu","ov8-sheng-siong","1d0-kimly","558-ums","1f2-union-gas","s68-sgx","awx-aem","d05-dbs","5g3-talkmed"]}
    lambda_handler(context, None)