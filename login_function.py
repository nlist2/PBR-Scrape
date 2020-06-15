def pbr_login(sess):
    loginurl = 'https://www.prepbaseballreport.com/customer/account/login/'
    loginaction = 'https://www.prepbaseballreport.com/customer/account/loginPost/'
    # session = sess
    r1 = sess.get(loginurl)
    logsoup = BeautifulSoup(r1.text, 'html.parser')
    form_key = logsoup.select_one('#login-form input[name="form_key"]')['value']
    login_data = {'login[username]': 'mohammed246@cmailing.com',
    'login[password]': 'dinger2034', 'form_key': form_key}
    r = sess.post(loginaction, data=login_data, headers=dict(Referer=loginurl))
    # print(r.text)
    print('Login Success')
    return sess