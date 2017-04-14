var gulp = require('gulp');
var autoprefixer = require('gulp-autoprefixer');
var imagemin   = require('gulp-imagemin');
var jscs = require('gulp-jscs');
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var scsslint = require('gulp-scss-lint');
var sourcemaps = require('gulp-sourcemaps');
var uglify = require('gulp-uglify');
var del = require('del');

var sassOptions = {
    errLogToConsole: true,
    outputStyle: 'expanded'
};

// Make sure you update this for the specific browser requirements for your projct
// See https://github.com/ai/browserslist
var autoprefixerOptions = {
    browsers: ['last 2 versions', 'Firefox ESR', 'ie > 8']
};

var input = 'hra/static_src/';
var output = 'hra/static_compiled/';

var sass_input = input + 'css/**/*.scss';
var sass_output = output + 'css';
var js_input = input + 'js/**/*.js';
var js_output = output + 'js';
var image_input = input + 'images/**/*';
var image_output = output + 'images';
var vendor_input = input + 'vendor/**/*';
var vendor_output = output + 'vendor';

// Clean the output directory
gulp.task('clean', function() {
    return del(output + '/*', { force: true });
});

// Sass linting task.
gulp.task('scss-lint', function() {
    return gulp.src(sass_input)
        .pipe(scsslint({'maxBuffer':  400 * 1024}))
        .pipe(scsslint.failReporter());
});

// Sass development task - compiles css, adds sourcemaps for easier developer debugging,
// adds vendor prefixes, moves css files to the 'css' folder and outputs any
// errrors to the console
gulp.task('sass-dev', function() {
    return gulp
        .src(sass_input)
        .pipe(sass(sassOptions).on('error', sass.logError))
        .pipe(autoprefixer())
        .pipe(sourcemaps.init())
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(sass_output));
});

// Sass production task - compiles compressed css with no maps, adds
// vendor prefixes, moves the css files to the static_compiled folder.
gulp.task('sass-prod', function() {
    return gulp
        .src(sass_input)
        .pipe(sass({ outputStyle: 'compressed' }))
        .pipe(autoprefixer(autoprefixerOptions))
        .pipe(gulp.dest(sass_output));
});

// Check for invalid code with jshint
gulp.task('jshint', function() {
    // A .jshintrc config file can optionally be used to set config options
    return gulp.src(js_input)
        .pipe(jshint())
        .pipe(jshint.reporter());
});

// Check js coding style with jscs (airbnb presets)
// Config  is set in the .jscsrc file.
gulp.task('jscs', function() {
    return gulp.src(js_input)
        .pipe(jscs())
        .pipe(jscs.reporter())
        .pipe(jscs.reporter('fail'));
});

// JS development task - copies the files (uncompressed)
// to the static_compiled folder and adds sourcemaps for easier debugging.
gulp.task('js-dev', function() {
    return gulp
        .src(js_input)
        .pipe(sourcemaps.init())
        .pipe(sourcemaps.write('/maps'))
        .pipe(gulp.dest(js_output));
});

// JS production task which minifies the js. Copies to the static_compiled folder.
gulp.task('js-prod', function() {
    return gulp
        .src(js_input)
        .pipe(uglify())
        .pipe(gulp.dest(js_output));
});

// Image optimisation task
gulp.task('image-optimise', function() {
    return gulp.src(image_input)
        .pipe(imagemin())
        .pipe(gulp.dest(image_output));
});

// Copy vendor files to the output directory.
// These are assumed to be already compiled and minified.
gulp.task('vendor-files', function(){
    return gulp.src(vendor_input)
        .pipe(gulp.dest(vendor_output));
});


// Dev task which calls both sass and js development tasks, and also runs the linters
gulp.task('dev', ['clean', 'scss-lint', 'jscs', 'jshint', 'sass-dev', 'js-dev', 'vendor-files', 'image-optimise']);

// Live recompile of sass and js when working
// It will do an initial build to pick up changes since it last ran.
gulp.task('watch', ['dev'], function() {
    gulp
        // Watch the sass_input folder for change,
        // and run `sass` task when something happens
        .watch(sass_input, ['sass-dev'])
        // When there is a change,
        // log a message in the console
        .on('change', function(event) {
            console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
        });
    gulp
        //similar pattern for the js folder.
        .watch(js_input,['js-dev'])
        .on('change', function(event) {
            console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
        });
});

// Production task - clears out the destination repo (which gets rid of maps etc), lints
// and runs production tasks
gulp.task('prod', ['clean', 'sass-prod', 'js-prod', 'image-optimise', 'vendor-files']);
