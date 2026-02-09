/**
 * Gulpfile for Visual Framework SCSS compilation
 * Compiles SCSS from VF-Core and custom styles into CSS
 */

const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const postcss = require('gulp-postcss');
const autoprefixer = require('autoprefixer');
const cssnano = require('cssnano');
const sourcemaps = require('gulp-sourcemaps');
const rename = require('gulp-rename');
const path = require('path');

// Paths configuration
const paths = {
  scss: {
    src: 'src/scss/**/*.scss',
    main: 'src/scss/main.scss',
    dest: 'api/static/css'
  },
  assets: {
    dest: 'api/static/assets'
  }
};

// SCSS compilation
function compileSCSS() {
  return gulp.src(paths.scss.main)
    .pipe(sourcemaps.init())
    .pipe(sass({
      includePaths: [
        'node_modules',
        'node_modules/@visual-framework'
      ],
      outputStyle: 'expanded',
      silenceDeprecations: ['legacy-js-api']
    }).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer()
    ]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(paths.scss.dest));
}

// Minified CSS for production
function minifyCSS() {
  return gulp.src(paths.scss.main)
    .pipe(sass({
      includePaths: [
        'node_modules',
        'node_modules/@visual-framework'
      ],
      outputStyle: 'compressed',
      silenceDeprecations: ['legacy-js-api']
    }).on('error', sass.logError))
    .pipe(postcss([
      autoprefixer(),
      cssnano()
    ]))
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.scss.dest));
}

// Copy VF design tokens
function copyAssets() {
  return gulp.src([
    'node_modules/@visual-framework/vf-design-tokens/dist/**/*'
  ], { allowEmpty: true })
    .pipe(gulp.dest('api/static/design-tokens'));
}

// Watch for changes
function watchFiles() {
  gulp.watch(paths.scss.src, gulp.series(compileSCSS, minifyCSS));
}

// Clean task (using del)
async function clean() {
  const { deleteSync } = await import('del');
  return deleteSync([
    'api/static/css/**',
    'api/static/js/**',
    'api/static/assets/**',
    'api/static/design-tokens/**'
  ]);
}

// Define tasks
const build = gulp.series(
  gulp.parallel(compileSCSS, minifyCSS, copyAssets)
);

const watch = gulp.series(build, watchFiles);

// Export tasks
exports.clean = clean;
exports.scss = compileSCSS;
exports.minify = minifyCSS;
exports.assets = copyAssets;
exports.build = build;
exports.watch = watch;
exports.default = build;
