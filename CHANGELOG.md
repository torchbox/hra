0.29.hra71.test1 (2017-12-04)
-----------------------------

- HRA-71 Try to trigger middleware exceptions that are failing silently


0.29 (2017-12-04)
-----------------

- HRA-15 Monkeypatch Wagtail Sitemap to avoid timeout (#117)
- HRA-63 Missed opacity change in newsletter signup placeholder (#113)
- HRA-66 Adjust glossary tab based on further testing (#115)
- HRA-70 Remove unwanted <br/> added by hallo.js in cookie banner (#114)
- HRA-73 Fix glossary tab page overflow on iPad (#116)
- HRA-76 Fix regression in search filter checkbox spacing (#118)


0.28 (2017-11-27)
-----------------

- HRA-1 Remove unwanted tags on paste to avoid triggering WAF (#104)
- HRA-3 Add feedback "popup" (#106)
- HRA-5 Improve efficiency of REC index page (#109)
- HRA-6 Add lots of favicons (#108)
- HRA-7 Use new reCAPTCHA version (#103)
- HRA-14 Avoid JavaScript error on non-glossary pages (#105)
- HRA-15 Fix sitemap.xml (#107)
- HRA-18 Accessibility audit actions (#111)
- HRA-70 Adjust notification length/style to fit cookie banner (#112)
- Fix some flake8 warnings (#110)


0.27 (2017-11-08)
-----------------

- add pod anti-affinity for even zone distribution
- reduce processes per container
- revert to console logging
- chart fixage

0.26 (2017-11-06)
-----------------

- Bugfixes to secret keys
- Logging refinements


0.25 (2017-11-03)
-----------------

- Add authentication to watchtower


0.24 (2017-11-03)
-----------------

- use watchtower


0.23 (2017-11-03)
-----------------

- region typo


0.22 (2017-11-03)
-----------------

- fix le bugs in watchtower


0.21 (2017-11-03)
-----------------

- bump raven client


0.20 (2017-11-03)
-----------------

- Add helm package
- Stop using `dj_database_url` and `django_cache_url`
- integrate watchtower


0.19 (2017-10-05)
-----------------

- Update google tag tracking code


0.18 (2017-10-05)
-----------------

- Integrate sentry


0.17 (2017-10-05)
-----------------

- Applied all changes from master


0.16 (2017-10-05)
-----------------

- Add new GTM ID


0.15 (2017-10-03)
-----------------

- Add HARP API to production settings
- Merge ongoing dev changes


0.14 (2017-10-02)
-----------------

- ok, http: is required.


0.13 (2017-10-02)
-----------------

- OK, lets try insecure S3 urls!


0.12 (2017-10-02)
-----------------

- Make `AWS_S3_URL_PROTOCOL` an empty string


0.11 (2017-09-27)
-----------------

- Change elasticsearch settings to mirror others on platform
- Ensure the ES Index can be varied between production/stage

0.10 (2017-09-27)
-----------------

- Add version file to docker image
- Set S3 uploads to public-read, because we're not using OAI
- Change S3 protocol to https


0.9 (2017-09-04)
----------------

- Fix typo in Dockerfile


0.8 (2017-09-01)
----------------

- Simplify starting container


0.7 (2017-09-01)
----------------

- add recaptcha to prod settings


0.6 (2017-09-01)
----------------

- getting a bit bored of base64 if i am completely honest


0.5 (2017-09-01)
----------------

- more base64 fixes


0.4 (2017-09-01)
----------------

- python 3 base64 decode


0.3 (2017-09-01)
----------------

- remove reference to manifest.json


0.2 (2017-09-01)
----------------

- Basic Auth fixes


0.1 (2017-09-01)
----------------
