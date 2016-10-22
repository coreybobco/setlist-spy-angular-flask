// Generated on 2016-10-03 using generator-angular 0.15.1
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/***REMOVED***,*/***REMOVED****.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) ***REMOVED***

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // Automatically load required Grunt tasks
  require('jit-grunt')(grunt, ***REMOVED***
    useminPrepare: 'grunt-usemin',
    ngtemplates: 'grunt-angular-templates',
    cdnify: 'grunt-google-cdn'
  ***REMOVED***);

  // Configurable paths for the application
  var appConfig = ***REMOVED***
    app: require('./bower.json').appPath || 'app',
    dist: 'dist'
  ***REMOVED***;
  var serveStatic = require('serve-static');
  // Define the configuration for all the tasks
  grunt.initConfig(***REMOVED***

    // Project settings
    yeoman: appConfig,
    ec2: 'ec2.json'

    // Watches files for changes and runs tasks based on the changed files
    watch: ***REMOVED***
      bower: ***REMOVED***
        files: ['bower.json'],
        tasks: ['wiredep']
      ***REMOVED***,
      js: ***REMOVED***
        files: ['<%= yeoman.app %>/scripts/***REMOVED***,*/***REMOVED****.js'],
        tasks: ['newer:jshint:all', 'newer:jscs:all'],
        options: ***REMOVED***
          livereload: '<%= connect.options.livereload %>'
        ***REMOVED***
      ***REMOVED***,
      jsTest: ***REMOVED***
        files: ['test/spec/***REMOVED***,*/***REMOVED****.js'],
        tasks: ['newer:jshint:test', 'newer:jscs:test', 'karma']
      ***REMOVED***,
      styles: ***REMOVED***
        files: ['<%= yeoman.app %>/styles/***REMOVED***,*/***REMOVED****.css'],
        tasks: ['newer:copy:styles', 'postcss']
      ***REMOVED***,
      gruntfile: ***REMOVED***
        files: ['Gruntfile.js']
      ***REMOVED***,
      livereload: ***REMOVED***
        options: ***REMOVED***
          livereload: '<%= connect.options.livereload %>'
        ***REMOVED***,
        files: [
          '<%= yeoman.app %>/***REMOVED***,*/***REMOVED****.html',
          '.tmp/styles/***REMOVED***,*/***REMOVED****.css',
          '<%= yeoman.app %>/images/***REMOVED***,*/***REMOVED****.***REMOVED***png,jpg,jpeg,gif,webp,svg***REMOVED***'
        ]
      ***REMOVED***
    ***REMOVED***,

    injector: ***REMOVED***
      options: ***REMOVED***
        ignorePath: "app/"
      ***REMOVED***,
      local_dependencies: ***REMOVED***
        files: ***REMOVED***
          '<%= yeoman.app %>/index.html': [
            '<%= yeoman.app %>/scripts/jbooklet/*.js',
            '<%= yeoman.app %>/scripts/jbooklet/*.css'
          ]
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***,

    // The actual grunt server settings
    connect: ***REMOVED***
      options: ***REMOVED***
        port: 9000,
        // Change this to '0.0.0.0' to access the server from outside.
        hostname: '0.0.0.0',
        livereload: 35729
      ***REMOVED***,
      proxies: [
        ***REMOVED***
          context: '/addGene',
          host: '127.0.0.1',
          port: 5000,
          https: false,
          changeOrigin: false,
          xforward: false
        ***REMOVED***,
        ***REMOVED***
          context: '/mutate',
          host: '127.0.0.1',
          port: 5000,
          https: false,
          changeOrigin: false,
          xforward: false
        ***REMOVED***
      ],
      livereload: ***REMOVED***
        options: ***REMOVED***
          open: true,
          middleware: function (connect) ***REMOVED***
            return [
              require('grunt-connect-proxy/lib/utils').proxyRequest,
            serveStatic('.tmp'),
              connect().use(
                '/bower_components',
                serveStatic('./bower_components')
              ),
              connect().use(
                '/app/styles',
                serveStatic('./app/styles')
              ),
              serveStatic(appConfig.app)
            ];
          ***REMOVED***
        ***REMOVED***
      ***REMOVED***,
      test: ***REMOVED***
        options: ***REMOVED***
          port: 9001,
          middleware: function (connect) ***REMOVED***
            return [
              serveStatic('.tmp'),
              serveStatic('test'),
              connect().use(
                '/bower_components',
                serveStatic('./bower_components')
              ),
              serveStatic(appConfig.app)
            ];
          ***REMOVED***
        ***REMOVED***
      ***REMOVED***,
      dist: ***REMOVED***
        options: ***REMOVED***
          open: true,
          base: '<%= yeoman.dist %>'
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***,

    // Make sure there are no obvious mistakes
    jshint: ***REMOVED***
      options: ***REMOVED***
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      ***REMOVED***,
      all: ***REMOVED***
        src: [
          'Gruntfile.js',
          '<%= yeoman.app %>/scripts/***REMOVED***,*/***REMOVED****.js'
        ]
      ***REMOVED***,
      test: ***REMOVED***
        options: ***REMOVED***
          jshintrc: 'test/.jshintrc'
        ***REMOVED***,
        src: ['test/spec/***REMOVED***,*/***REMOVED****.js']
      ***REMOVED***
    ***REMOVED***,

    // Make sure code styles are up to par
    jscs: ***REMOVED***
      options: ***REMOVED***
        config: '.jscsrc',
        verbose: true
      ***REMOVED***,
      all: ***REMOVED***
        src: [
          'Gruntfile.js',
          '<%= yeoman.app %>/scripts/***REMOVED***,*/***REMOVED****.js'
        ]
      ***REMOVED***,
      test: ***REMOVED***
        src: ['test/spec/***REMOVED***,*/***REMOVED****.js']
      ***REMOVED***
    ***REMOVED***,

    // Empties folders to start fresh
    clean: ***REMOVED***
      dist: ***REMOVED***
        files: [***REMOVED***
          dot: true,
          src: [
            '.tmp',
            '<%= yeoman.dist %>/***REMOVED***,*/***REMOVED****',
            '!<%= yeoman.dist %>/.git***REMOVED***,*/***REMOVED****'
          ]
        ***REMOVED***]
      ***REMOVED***,
      server: '.tmp'
    ***REMOVED***,

    // Add vendor prefixed styles
    postcss: ***REMOVED***
      options: ***REMOVED***
        processors: [
          require('autoprefixer')(***REMOVED***browsers: ['last 1 version']***REMOVED***)
        ]
      ***REMOVED***,
      server: ***REMOVED***
        options: ***REMOVED***
          map: true
        ***REMOVED***,
        files: [***REMOVED***
          expand: true,
          cwd: '.tmp/styles/',
          src: '***REMOVED***,*/***REMOVED****.css',
          dest: '.tmp/styles/'
        ***REMOVED***]
      ***REMOVED***,
      dist: ***REMOVED***
        files: [***REMOVED***
          expand: true,
          cwd: '.tmp/styles/',
          src: '***REMOVED***,*/***REMOVED****.css',
          dest: '.tmp/styles/'
        ***REMOVED***]
      ***REMOVED***
    ***REMOVED***,

    // Automatically inject Bower components into the app
    wiredep: ***REMOVED***
      app: ***REMOVED***
        src: ['app/index.html'],
          dependencies: true,
          devDependencies: true
          // ...
      ***REMOVED***,
      test: ***REMOVED***
        devDependencies: true,
        src: '<%= karma.unit.configFile %>',
        ignorePath:  /\.\.\//,
        fileTypes:***REMOVED***
          js: ***REMOVED***
            block: /(([\s\t]*)\/***REMOVED***2***REMOVED***\s*?bower:\s*?(\S*))(\n|\r|.)*?(\/***REMOVED***2***REMOVED***\s*endbower)/gi,
              detect: ***REMOVED***
                js: /'(.*\.js)'/gi
              ***REMOVED***,
              replace: ***REMOVED***
                js: '\'***REMOVED******REMOVED***filePath***REMOVED******REMOVED***\','
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***
      ***REMOVED***
    ***REMOVED***,

    // Renames files for browser caching purposes
    filerev: ***REMOVED***
      dist: ***REMOVED***
        src: [
          '<%= yeoman.dist %>/scripts/***REMOVED***,*/***REMOVED****.js',
          '<%= yeoman.dist %>/styles/***REMOVED***,*/***REMOVED****.css',
          '<%= yeoman.dist %>/images/***REMOVED***,*/***REMOVED****.***REMOVED***png,jpg,jpeg,gif,webp,svg***REMOVED***',
          '<%= yeoman.dist %>/styles/fonts/*'
        ]
      ***REMOVED***
    ***REMOVED***,

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: ***REMOVED***
      html: '<%= yeoman.app %>/index.html',
      options: ***REMOVED***
        dest: '<%= yeoman.dist %>',
        flow: ***REMOVED***
          html: ***REMOVED***
            steps: ***REMOVED***
              js: ['concat', 'uglifyjs'],
              css: ['cssmin']
            ***REMOVED***,
            post: ***REMOVED******REMOVED***
          ***REMOVED***
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***,

    // Performs rewrites based on filerev and the useminPrepare configuration
    usemin: ***REMOVED***
      html: ['<%= yeoman.dist %>/***REMOVED***,*/***REMOVED****.html'],
      css: ['<%= yeoman.dist %>/styles/***REMOVED***,*/***REMOVED****.css'],
      js: ['<%= yeoman.dist %>/scripts/***REMOVED***,*/***REMOVED****.js'],
      options: ***REMOVED***
        assetsDirs: [
          '<%= yeoman.dist %>',
          '<%= yeoman.dist %>/images',
          '<%= yeoman.dist %>/styles'
        ],
        patterns: ***REMOVED***
          js: [[/(images\/[^''""]*\.(png|jpg|jpeg|gif|webp|svg))/g, 'Replacing references to images']]
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***,

    // The following *-min tasks will produce minified files in the dist folder
    // By default, your `index.html`'s <!-- Usemin block --> will take care of
    // minification. These next options are pre-configured if you do not wish
    // to use the Usemin blocks.
    // cssmin: ***REMOVED***
    //   dist: ***REMOVED***
    //     files: ***REMOVED***
    //       '<%= yeoman.dist %>/styles/main.css': [
    //         '.tmp/styles/***REMOVED***,*/***REMOVED****.css'
    //       ]
    //     ***REMOVED***
    //   ***REMOVED***
    // ***REMOVED***,
    // uglify: ***REMOVED***
    //   dist: ***REMOVED***
    //     files: ***REMOVED***
    //       '<%= yeoman.dist %>/scripts/scripts.js': [
    //         '<%= yeoman.dist %>/scripts/scripts.js'
    //       ]
    //     ***REMOVED***
    //   ***REMOVED***
    // ***REMOVED***,
    // concat: ***REMOVED***
    //   dist: ***REMOVED******REMOVED***
    // ***REMOVED***,

    imagemin: ***REMOVED***
      dist: ***REMOVED***
        files: [***REMOVED***
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '***REMOVED***,*/***REMOVED****.***REMOVED***png,jpg,jpeg,gif***REMOVED***',
          dest: '<%= yeoman.dist %>/images'
        ***REMOVED***]
      ***REMOVED***
    ***REMOVED***,

    svgmin: ***REMOVED***
      dist: ***REMOVED***
        files: [***REMOVED***
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '***REMOVED***,*/***REMOVED****.svg',
          dest: '<%= yeoman.dist %>/images'
        ***REMOVED***]
      ***REMOVED***
    ***REMOVED***,

    htmlmin: ***REMOVED***
      dist: ***REMOVED***
        options: ***REMOVED***
          collapseWhitespace: true,
          conservativeCollapse: true,
          collapseBooleanAttributes: true,
          removeCommentsFromCDATA: true
        ***REMOVED***,
        files: [***REMOVED***
          expand: true,
          cwd: '<%= yeoman.dist %>',
          src: ['*.html'],
          dest: '<%= yeoman.dist %>'
        ***REMOVED***]
      ***REMOVED***
    ***REMOVED***,

    ngtemplates: ***REMOVED***
      dist: ***REMOVED***
        options: ***REMOVED***
          module: 'markovmutatorApp',
          htmlmin: '<%= htmlmin.dist.options %>',
          usemin: 'scripts/scripts.js'
        ***REMOVED***,
        cwd: '<%= yeoman.app %>',
        src: 'views/***REMOVED***,*/***REMOVED****.html',
        dest: '.tmp/templateCache.js'
      ***REMOVED***
    ***REMOVED***,

    // ng-annotate tries to make the code safe for minification automatically
    // by using the Angular long form for dependency injection.
    ngAnnotate: ***REMOVED***
      dist: ***REMOVED***
        files: [***REMOVED***
          expand: true,
          cwd: '.tmp/concat/scripts',
          src: '*.js',
          dest: '.tmp/concat/scripts'
        ***REMOVED***]
      ***REMOVED***
    ***REMOVED***,

    // Replace Google CDN references
    cdnify: ***REMOVED***
      dist: ***REMOVED***
        html: ['<%= yeoman.dist %>/*.html']
      ***REMOVED***
    ***REMOVED***,

    // Copies remaining files to places other tasks can use
    copy: ***REMOVED***
      dist: ***REMOVED***
        files: [***REMOVED***
          expand: true,
          dot: true,
          cwd: '<%= yeoman.app %>',
          dest: '<%= yeoman.dist %>',
          src: [
            '*.***REMOVED***ico,png,txt***REMOVED***',
            '*.html',
            'images/***REMOVED***,*/***REMOVED****.***REMOVED***webp***REMOVED***',
            'styles/fonts/***REMOVED***,*/***REMOVED****.*'
          ]
        ***REMOVED***, ***REMOVED***
          expand: true,
          cwd: '.tmp/images',
          dest: '<%= yeoman.dist %>/images',
          src: ['generated/*']
        ***REMOVED***, ***REMOVED***
          expand: true,
          cwd: 'bower_components/bootstrap/dist',
          src: 'fonts/*',
          dest: '<%= yeoman.dist %>'
        ***REMOVED***]
      ***REMOVED***,
      styles: ***REMOVED***
        expand: true,
        cwd: '<%= yeoman.app %>/styles',
        dest: '.tmp/styles/',
        src: '***REMOVED***,*/***REMOVED****.css'
      ***REMOVED***
    ***REMOVED***,

    // Run some tasks in parallel to speed up the build process
    concurrent: ***REMOVED***
      server: [
        'copy:styles'
      ],
      test: [
        'copy:styles'
      ],
      dist: [
        'copy:styles',
        'imagemin',
        'svgmin'
      ]
    ***REMOVED***,

    // Test settings
    karma: ***REMOVED***
      unit: ***REMOVED***
        configFile: 'test/karma.conf.js',
        singleRun: true
      ***REMOVED***
    ***REMOVED***
  ***REMOVED***);

  grunt.loadNpmTasks('grunt-injector');
  grunt.loadNpmTasks('grunt-wiredep');
  grunt.loadNpmTasks('grunt-connect-proxy');

  grunt.registerTask('serve', 'Compile then start a connect web server', function (target) ***REMOVED***
    if (target === 'dist') ***REMOVED***
      return grunt.task.run(['build', 'connect:dist:keepalive']);
    ***REMOVED***

    grunt.task.run([
      'clean:server',
      'wiredep',
      'configureProxies:server',
      'concurrent:server',
      'postcss:server',
      'connect:livereload',
      'watch'
    ]);
  ***REMOVED***);

  grunt.registerTask('server', 'DEPRECATED TASK. Use the "serve" task instead', function (target) ***REMOVED***
    grunt.log.warn('The `server` task has been deprecated. Use `grunt serve` to start a server.');
    grunt.task.run(['serve:' + target]);
  ***REMOVED***);

  grunt.registerTask('test', [
    'clean:server',
    'wiredep',
    'concurrent:test',
    'postcss',
    'connect:test',
    'karma'
  ]);

  grunt.registerTask('build', [
    'clean:dist',
    'wiredep',
    'useminPrepare',
    'concurrent:dist',
    'postcss',
    'ngtemplates',
    'concat',
    'ngAnnotate',
    'copy:dist',
    'cdnify',
    'cssmin',
    'uglify',
    'filerev',
    'usemin',
    'htmlmin'
  ]);

  grunt.registerTask('default', [
    'newer:jshint',
    'newer:jscs',
    'test',
    'build'
  ]);

***REMOVED***;
