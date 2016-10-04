'use strict';

describe('Controller: AboutCtrl', function () ***REMOVED***

  // load the controller's module
  beforeEach(module('markovmutatorApp'));

  var AboutCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) ***REMOVED***
    scope = $rootScope.$new();
    AboutCtrl = $controller('AboutCtrl', ***REMOVED***
      $scope: scope
      // place here mocked dependencies
    ***REMOVED***);
  ***REMOVED***));

  it('should attach a list of awesomeThings to the scope', function () ***REMOVED***
    expect(AboutCtrl.awesomeThings.length).toBe(3);
  ***REMOVED***);
***REMOVED***);
