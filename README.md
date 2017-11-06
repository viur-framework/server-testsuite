# README #

First draft for an viur instance, which tests itself.

### What is this repository for? ###

* Running testcases on specific viur server features
* Version: 0.0.3

How do I get set up:

	git submodule init
	git submodle update
	
start the instance locally, e.g on port 9090

	cd appengine
	dev_appserver.py --log_level debug --storage_path ../storage . --admin_port 9095 --port 9090 -A server-testsuite-viur
	
Remember the username and password you get on the terminal output. Providing a password file called 'credentials.ini' at top directory of this project in ini format:

	[server-testsuite-viur]
    username: admin@server-testsuite-viur.appspot.com
    password: yourPasswordHere
    base_url: http://localhost:9090

Test dependencies:

	sudo pip2.7 install requests

Runnig unittests:	

	cd path/to/testcase_viur
	python -m tests.all_suites

you should see something like that:
	
	test00 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser0.firstname. report refKeys and changedate should be updated ... ok
	test01 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser0.lastname. report refKeys and changedate should not be updated ... ok
	test02 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser1.firstname. report refKeys and changedate should not be updated ... ok
	test03 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser1.lastname. report refKeys and changedate should not be updated ... ok
	test04 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser2.firstname. report refKeys and changedate should not be updated ... ok
	test05 (tests.viur_relations.update_level.UpdateLevelTest)
	Change testUser1.lastname. report refKeys and changedate should not be updated ... ok
	test06 (tests.viur_relations.update_level.UpdateLevelTest)
	Calling updateSearchIndex on report kind and check if all updateLevels are ok. report changedate should have changed ... ok
	test07 (tests.viur_relations.update_level.UpdateLevelTest)
	Changing firstname of testUser0 and check again ... ok
	test08 (tests.viur_relations.update_level.UpdateLevelTest)
	Calling updateSearchIndex on user kind. ... ok
	test09 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if testUser3.firstname gets propagated to viur_relations and report entry in a multiple setting ... ok
	test10 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if testUser3.lastname does not change neither report nor viur relations ... ok
	test11 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if testUser4.firstname gets updated, but neither in vuir_relations nor in report.updatelevel4_multi ... ok
	test12 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if testUser4.lastname gets updated, but neither in vuirRelations nor in report.updatelevel4_multi ... ok
	test13 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if testUser5.firstname gets updated, but neither in vuirRelations nor in report.updatelevel4_multi ... ok
	test14 (tests.viur_relations.update_level.UpdateLevelTest)
	Check if updateSearchIndex updates testUser3 and testUser4 in viur_relations and report for multiple relational bones ... ok
	
	----------------------------------------------------------------------
	Ran 15 tests in 105.081s
	
	OK


### Contribution guidelines ###

Please implement testcases for each bone and its features. Group them as stacked testsuites as in tests.viur_relations.update_level


### Who do I talk to? ###

* coding: https://github.com/skoegl
