# My School Hub
By Hub App Ltd.

My School Hub brings together students, parents and teachers in school communities throughout New Zealand. The app is offered in 2 versions. One version is called DIOHUB which works partnership with Diocesan School, and is available for all DIO parents and teachers, as well as students in Year 11 and above. The other version called My School Hub is an 'open' version that is available to all schools in New Zealand.

## Technical Documentation

Please refer to Hub App - Technical Docs and Hub App - Cloud Ops Guide on SharePoint for detailed configuration notes and account credentials.

3 environments are available for My School Hub: dev, stage and prod.

## Build & Run `appv4` For Dev
1. Make sure the `Node.js` and `npm` are installed and then install `ionic` and `cordova` globally.
2. Clone the repository and then do `npm install` to install all dependencies.
3. Run `ionic cordova platform add ios` and `ionic cordova platform add android` to add the iOS and Android platforms.
4. For running iOS app on the simulator, you can either run `ionic cordova run ios -l` or open your XCode and select the `platform/ios` folder.
* You may get some CocoaPod errors when you try to build and run the app, it is because CocoaPod is used by `phonegap-plugin-push` plugin. Please have a look at `https://github.com/phonegap/phonegap-plugin-push/blob/master/docs/INSTALLATION.md#ios-details` for the  fixes.
* Errors may look like:
- CocoaPod Disk Space
- Library not found for -lPods-Appname
- Library not found for -lGoogleToolboxForMac
- Module FirebaseInstanceID not found

## Publishing Server Changes (Database, API and/or Web Portal)

These steps were tested with:

* Windows 10 Pro: npm v6.4.1, node v8.16.0, Visual Studio 2017.
* Mac OS X 10.14.5: npm v6.4.1, node v8.14.0, Cordova CLI v8.1.2, Ionic CLI v4.5.0.

### Step 1. Build Web Portal

NodeJS required - install from https://nodejs.org/en/download/

1. Go to web portal project folder: `cd Documents\GitHub\Hub\webPortal`
2. Download libraries/node modules: `npm install`
3. Generate dist folder: `grunt build`
4. In HubApi project in Visual Studio, Build > Publish will now include web portal

### Step 2. Apply Database Changes

If there are database changes to apply, run a database migration script. This script is normally provided in the repository (from v1.0 onwards).

To generate a database migration script:
1. In Visual Studio, update `web.config` to point to the target database temporarily.
2. In Package Manager Console, run `Update-Database -script`.
3. If you get an error saying that the script cannot be generated because it may cause data loss, run `Update-Database -script -force` to generate the script, but double-check the output to see which field may cause data loss and the impact of this on the prod database.
4. Now run the script against the database.

Check developer notes to see if there are any initial data to configure or run, in addition to database migrations.

If applying changes to a production database, please apply them around the same time as you do the API swap from stage to prod. The API would be unavailable while there's a version mismatch between the API and database.

### Step 3. Publish API and Web Portal

Developers could publish to dev and stage directly from Visual Studio.

Make sure that you've deployed the Release (not Debug) configuration. You can obtain the publish profiles (\*.PublishSettings file) from Azure Portal.

For Prod environment:

1. All changes must be code reviewed and tested first. Prepare SQL script for database changes and test this in staging or copy of production database first.
2. Schedule a maintenance window and communicate this with the customer.
3. At start of maintenance window, take a database backup and stop scheduled tasks (logic apps).
4. Ops must publish to stage environment first (which is a deployment slot on the same web app as Prod), test that the build works and warm up environment, then make a swap to prod in Azure Portal.
5. Apply database changes (see above) at this time, plus changes to application settings, logic apps and other components (if any).
6. Start scheduled tasks.
7. Test: Log into web portal and open jobs list to confirm that the API is functional.
8. Communicate with customer that upgrade has completed.

## Publishing Mobile App Changes - v1 or v2

1. Update version number in `config.xml`
2. Check `$rootScope.environmentId` points to the required environment.
3. In Terminal, run `gulp sass` to make sure the CSS reflects latest stylesheets (AngularJS only).
4. Angular: Debug Build: `npm run build` or, Release Build with lint: `npm run build-prod`, followed by `cordova prepare`. Or AngularJS: Run `cordova prepare` for dev builds, `cordova prepare --release` for stage and prod builds. The release build minifies CSS and scripts.
5. iOS: In Xcode, Build > Archive. In workspace settings, select build with legacy build system due to a Cordova compatibility issue.
6. iOS: In Xcode Organiser, submit to App Store for TestFlight and/or public store submissions, or create ad-hoc distribution build.
7. iOS: Complete remaining store listing metadata in iTunes Connect.
8. Android: In Android Studio, Build > Generate Signed APK. Upload to Google Play for beta or public store builds, or create ad-hoc distribution build. If opening project in Android Studio for the first time, select Import from Gradle, otherwise open project. Choose 'Remind me later' if asked to upgrade Gradle.
9. Android: Complete remaining store listing metadata in Google Play Developer Console.

## Publishing Mobile App Changes - v4
1. Update version number in `config.xml`
2. // * Update angular.json fileReplacements array (for now this is commented out when running prod build)
3. In terminal, run `ionic cordova run ios -l` for live debug running of the app. You can also speicify the target to run on desired simulators. e.g. `ionic cordova run ios -l -target='30AC9697-C3B4-4206-AB15-261E1F4A447B'`. You can use `cordova run ios --list` to see all available targets.
4. Run `ionic build --prod` for production build.
5. Then generate archive or apk file for the app as usual.

Record each public release (Server and/or Mobile) in GitHub.
Ad-hoc or TestFlight releases do not need to be recorded in GitHub.

## Upgrading Cordova Platform and Plugins

If upgrading Cordova platforms (iOS, Android), please re-apply the following changes:

1. `app/platforms/android/res/drawable/notification_icon.png`
2. Select Xcode provisioning profiles
3. In Xcode > Project > Capabilities, enable Associated Domains and add domain `applinks:get.myschoolhub.co.nz`.

All other files should've already been copied as part of the base project or plugins. Check that app icons and splash screens have been applied.

## Universal Links

Installing `ionic-plugin-deeplinks` requires the following parameters:

`cordova plugin add ionic-plugin-deeplinks --variable URL_SCHEME=nz.hubapp.myschool --variable DEEPLINK_SCHEME=https --variable DEEPLINK_HOST=get.myschoolhub.co.nz --variable ANDROID_PATH_PREFIX=/ --save`

This allows the user to open the app by navigating to https://get.myschoolhub.co.nz/ once website association has been configured by copying the files in `/webLanding/.well-known` folder, or via `nz.hubapp.myschool://` links. Confirm that site association files exist: https://get.myschoolhub.co.nz/.well-known/apple-app-site-association and https://get.myschoolhub.co.nz/.well-known/assetlinks.json

The get.myschoolhub.co.nz landing mini-website contains a single page and configuration to support universal app links. This is a workaround because the main website is running on a web hosting platform that does not support universal app links.

Universal app link only works when navigating to the site from a webpage in another domain or other source. It does not work if you're typing the URL directly into the browser. `apple-app-site-association` file must have Content-Type set to `application/json`.

## Publish Power BI Report

Data Source Settings - Dev:
Server: `hubdev.database.windows.net`
Database: `hubdev`

Data Source Settings - Prod:
Server: `hubapp.database.windows.net`
Database: `hubapp-prod`

1. Use the `db/Admin Report Views/* - Dev.pbix` files to edit reports in Power BI Desktop.
2. Publish the report to Power BI web portal to test it against the dev environment dataset.

Once you're ready to deploy report to production:
1. Copy the updated `db/Admin Report Views/* - Dev.pbix` file and replace the corresponding `db/Admin Report Views/* - Prod.pbix` file.
2. Open the `* - Prod.pbix` file in Power BI Desktop.
3. Select Edit Queries > Data Source Settings > Change Source, and update it to the prod settings above.
4. Click Apply Changes button.
5. Click Publish button, log in if needed, then it should prompt you to confirm replacing the 'Report - MySchoolHub - Prod' or 'Report View - Prod' (DIOHUB) dataset.

Only the `* - Dev.pbix` file is saved to repository, because the Prod version is a copy except for Data Source Settings.

## Maintain old versions

For running `gulp sass` for pre-v4 versions, use the node version v8 (normally v8.16.0) and for v4 use node version v10+ (currently v10.15.3).
For switching different node versions, please install nvm (https://github.com/nvm-sh/nvm).
Run `nvm install <version>` to install different node versions.
Run `nvm ls` to list all versions installed locally.
Run `nvm use <version>` to switch versions.
Please check the usage part for other usages.


## Development Process
DB Schema Changes
* If you need to do DB schema changes, you need to switch to the `db` branch and make only db related changes there using `-db` database for testing purpose.
* When you finish with the feature and get approved for merging your feature back to `dev`, then you can apply the changes to `-restore` database at that time. And notify other team members about it.
* Other team members can choose to do an update from `db` or `dev` branch. (Merge from `db` would be easier due to less changes)

Develop A New Feature
* When starting developing a new feature, create a branch from `dev` and called `feature/…`, and might need to do a merge from other branches for the features you need
* When finishing developing the feature, you need to create a pull request from your feature branch to `dev` and mention the pull request in the ticket comments. (Remember to resolve any conflicts for that pull request)
* The pull request name should looks like `<ticket number> + <ticket title/summary>`, for example `DEVF2-255 Add Comments Button`.
* Change the ticket status to  `Ready For Code Review` and assign the ticket to the reviewer.
* Once the code review process finishes and your code get approved to merge back to `dev`, then you need to do a `Squash and merge`.
* And after it has been successfully merged back to `dev`, then delete your feature branch.
