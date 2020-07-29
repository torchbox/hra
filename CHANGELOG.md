1.0.23 (2020-07-29)
-------------------

- HRA-218 Hero text background
- HRA-217 fix top level nav (#173)


1.0.22 (2020-05-14)
-------------------

- Upgrade from Django 1.11.27 to 1.11.29 (#162)
- HRA-200 update cookie banner (#159)
- HRA-199 New approvals specialist field (#158)


1.0.21 (2020-01-27)
-------------------

- Update LMS login form to point at .co.uk instead of .host (#157)


1.0.20 (2019-12-18)
-------------------

- Update Django version to 1.11.27 for CVE-2019-19844


1.0.19 (2019-07-03)
-------------------

- HRA-190 Avoid search indexing bug in TableBlock (#145)


1.0.18 (2019-05-09)
-------------------

- HRA-169 Tweaked order of Approvals and REC sections in REC Directory


1.0.17 (2019-03-27)
-------------------

- HRA-169 Removed HRA Office, added two new Approvals fields to REC Directory


1.0.16 (2019-03-14)
-------------------

- Fix CircleCI filters to test and deploy tags


1.0.15 (2019-03-14)
-------------------

- HRA-162 Fix all occurrences of page number validation (#139)
- HRA-163 Fix error when latest meeting for RECs is before this month (#141)
- Devops improvements (#138)
- Sentry upgrade and fix version tracking (#140)


1.0.14 (2019-03-11)
-------------------

- HRA-84 Clearer date validation in HARP import command (#133)
- HRA-95 Fix error when non-integer page number in URL (#132)
- HRA-133 Improve robustness of HARP logging (#130)
- HRA-141 Fix S3 file delete on overwrite leaving broken document (#137)
- HRA-148 Fix REC not shown if no future meeting dates (#135)


1.0.13 (2018-12-19)
-------------------

- HRA-133 Enable more HARP logging (#129)


1.0.12 (2018-11-30)
-------------------

- HRA-127 Add LMS Login block
- Pin django-redis dependency


1.0.11 (2018-10-30)
-------------------

- HRA-125 Hide notification footer
- HRA-126 Bump Django version on advisory


1.0.10 (2018-08-21)
-------------------

- HRA-119 upgrade to Django and Pillow


1.0.9 (2018-04-17)
------------------

- Update from raven 6.3.0 to 6.6.0 to hopefully fix error logging for Elasticsearch
https://github.com/getsentry/raven-python/issues/604


1.0.8 (2018-04-17)
------------------

- Update elastic search timeout from 10 to 30 seconds


1.0.7 (2018-03-19)
------------------

- Disable UWSGI request logging


1.0.6 (2018-03-15)
------------------

- Reduce log level


1.0.5 (2018-03-13)
------------------

- HRA-101 Reduce search chunk size to 50 (#124)
- Info log for research summaries import
- Fix to cronjobs/publish-scheduled-pages.yaml


1.0.4 (2018-03-02)
------------------

- Integration with k8s-safe-cronjob and add error reporting


1.0.3 (2018-03-02)
------------------

- Add k8s-safe-cronjob


1.0.2 (2018-02-08)
------------------

- HRA-94 Correct date format for research summaries search with pagination


1.0.1 (2018-02-08)
------------------

- HRA-93 Fix pagination with filters on search results
- HRA-93 Fix pagination with filters on research summaries


1.0.0 (2018-02-06)
------------------

- HRA-81 Fix for social image twitter url
- HRA-86 Add link from search to summaries
- HRA-86 Add REC opinion filter
- HRA-86 Add extra fields to research summaries index
- HRA-78 Back button on Committee page
- HRA-78 Add committee types and flags to committee page
- HRA-78 Remove England option
- HRA-72 Improved pagination


0.30 (2017-12-06)
-----------------

- HRA-15 Remove sitemap (#119)
- HRA-71 Stop basic auth middleware clobbering Wagtail preview requests (#120)
- HRA-73 Fix glossary tab page overflow on iPad (#116)
- HRA-76 Fix regression in search filter checkbox spacing (#118)
- HRA-78 Remove duplicate HRA Office heading
- HRA-67 Fix Glossary JavaScript error when no history state recorded
- Some flake8 fixes (#121)


0.29 (2017-12-04)
-----------------

- HRA-15 Monkeypatch Wagtail Sitemap to avoid timeout (#117)
- HRA-63 Missed opacity change in newsletter signup placeholder (#113)
- HRA-66 Adjust glossary tab based on further testing (#115)
- HRA-70 Remove unwanted <br/> added by hallo.js in cookie banner (#114)


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
