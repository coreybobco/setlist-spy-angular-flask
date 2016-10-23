/*
 * jBooklet jQuery Plugin
 * Copyright (c) 2014 Eugene Zlobin (http://zlobin.pro/zlobin_eng.html)
 *
 * Licensed under the MIT license (http://www.opensource.org/licenses/mit-license.php)
 *
 * Version : 2.4.6
 *
 * Originally based on the work of:
 *	1) Charles Mangin (http://clickheredammit.com/pageflip/)
 *	2) William Grauvogel (http://builtbywill.com/)
 */
(function (window, $, undefined) ***REMOVED***
  'use strict';

  $.fn.booklet = function(options) ***REMOVED***
    var $el = $(this),
        result = [],
        method,
        output,
        config,
        args = Array.prototype.slice.call(arguments, 1);

    // option type string - api call
    if (typeof options === 'string') ***REMOVED***
      $el.each(function() ***REMOVED***
        var obj = $el.data('jbooklet');

        if (obj) ***REMOVED***
          method = options;
          if (obj[method]) ***REMOVED***
            output = obj[method].apply(obj, args);
            if (output !== undefined || output) ***REMOVED***
              result.push(obj[method].apply(obj, args));
            ***REMOVED***
          ***REMOVED*** else ***REMOVED***
            $.error('Method "' + method + '" does not exist on jQuery.booklet.');
          ***REMOVED***
        ***REMOVED*** else ***REMOVED***
          $.error('jQuery.booklet has not been initialized. Method "' + options + '" cannot be called.');
        ***REMOVED***
      ***REMOVED***);

      if (result.length === 1) ***REMOVED***
        return result[0];
      ***REMOVED*** else if (result.length > 0) ***REMOVED***
        return result;
      ***REMOVED*** else ***REMOVED***
        return $el;
      ***REMOVED***
    ***REMOVED*** else if (typeof method === 'object' || !method) ***REMOVED***
      // else build new booklet
      return $el.each(function() ***REMOVED***
        var $element = $(this);
        var obj = $el.data('jbooklet');

        config = $.extend(***REMOVED******REMOVED***, $.fn.booklet.defaults, options);

        // destroy old booklet before creating new one
        if (obj) ***REMOVED***
          obj.destroy();
        ***REMOVED***

        // instantiate the booklet
        obj = new Booklet($element, config);
        obj.init();

        return this;
      ***REMOVED***);
    ***REMOVED***
  ***REMOVED***;

  function Booklet(target, inOptions) ***REMOVED***    
    var $wrapper = $('<div>', ***REMOVED***
          'class': 'b-page'
        ***REMOVED***),
        $underWrapper = $('<div>', ***REMOVED***
          'class': 'b-wrap'
        ***REMOVED***);
    $underWrapper.appendTo($wrapper);
    var options = inOptions,
        isInit = false,
        isBusy = false,
        isPlaying = false,
        isHoveringRight = false,
        isHoveringLeft = false,
        templates = ***REMOVED***
          //transparent item used with closed books
          blank: '<div class="b-page-blank"></div>'
        ***REMOVED***,
        css = ***REMOVED******REMOVED***, anim = ***REMOVED******REMOVED***,
        hoverShadowWidth, hoverFullWidth, hoverCurlWidth,
        pages = [], diff,
        originalPageTotal, startingPageNumber,
        // page content vars
        pN, p0, p1, p2, p3, p4, pNwrap, p0wrap, p1wrap, p2wrap, p3wrap, p4wrap, wraps,
       // control vars
        p3drag, p0drag,
        wPercent, wOrig, hPercent, hOrig,
        pWidth, pWidthN, pWidthH, pHeight, speedH,

        Page = function ($contentNode, index) ***REMOVED***
          var $el = $wrapper.clone();
          var $wrap = $el.find('.b-wrap');

          $el.addClass('b-page-' + index);
          if (!$contentNode.hasClass('b-page-empty')) ***REMOVED***
            if (index % 2 !== 0) ***REMOVED***
              $wrap.addClass('b-wrap-right');
            ***REMOVED*** else ***REMOVED***
              $wrap.addClass('b-wrap-left');
            ***REMOVED***
          ***REMOVED***
          $contentNode.appendTo($wrap);

          return ***REMOVED***
            index: index,
            contentNode: $contentNode[0],
            pageNode: $el[0]
          ***REMOVED***;
        ***REMOVED***,

        init = function () ***REMOVED***
          target.addClass('booklet');
          // store data for api calls
          target.data('jbooklet', this);

          // save original number of pages
          originalPageTotal = target.children().length;
          options.currentIndex = 0;

          if (originalPageTotal > 1000) ***REMOVED***
            options.manual = false;
          ***REMOVED***

          // generate page markup
          initPages();
          // initialize options
          updateOptions();
          // update after initialized
          updatePages();

          isInit = true;
        ***REMOVED***,
        destroy = function () ***REMOVED***
          // destroy all booklet items
          destroyControls();
          destroyPages();

          target.removeClass('booklet').removeData('booklet');

          isInit = false;
        ***REMOVED***,

        initPages = function () ***REMOVED***
          var nodes = [], newPage, i,
              children = target.children(),
              length = target.children().length;

          pages = [];

          // fix for odd number of pages
          if ((length % 2) !== 0) ***REMOVED***
            children.last().after(templates.blank);
          ***REMOVED***

          // set total page count
          options.pageTotal = length;
          startingPageNumber = 0;

          if (!isInit) ***REMOVED***
            options.currentIndex = 0;

            if (!isNaN(options.startingPage) && 
              options.startingPage <= options.pageTotal && 
              options.startingPage > 0) ***REMOVED***

              if ((options.startingPage % 2) !== 0) ***REMOVED***
                options.startingPage--;
              ***REMOVED***
              options.currentIndex = options.startingPage;
            ***REMOVED***
          ***REMOVED***

          // load pages
          for (i = 0; i < length; i++) ***REMOVED***
            newPage = new Page($(children[i]), i);

            nodes.push(newPage.pageNode);
            pages.push(newPage);
          ***REMOVED***
          target.append(nodes);
        ***REMOVED***,
        updatePages = function () ***REMOVED***
          updatePageStructure();
          updatePageCSS();
          updateManualControls();
        ***REMOVED***,
        updatePageStructure = function () ***REMOVED***
          var currIndex = options.currentIndex;

          // reset all content
          target.find('.b-page').removeClass('b-pN b-p0 b-p1 b-p2 b-p3 b-p4').hide();

          // add page classes
          if (currIndex - 2 >= 0) ***REMOVED***
            target.find('.b-page-' + (currIndex - 2)).addClass('b-pN').show();
            target.find('.b-page-' + (currIndex - 1)).addClass('b-p0').show();
          ***REMOVED***

          target.find('.b-page-' + (currIndex)).addClass('b-p1').show();
          target.find('.b-page-' + (currIndex + 1)).addClass('b-p2').show();

          if (currIndex + 3 <= options.pageTotal) ***REMOVED***
            target.find('.b-page-' + (currIndex + 2)).addClass('b-p3').show();
            target.find('.b-page-' + (currIndex + 3)).addClass('b-p4').show();
          ***REMOVED***

          // save structure elems to vars
          pN = target.find('.b-pN');
          p0 = target.find('.b-p0');
          p1 = target.find('.b-p1');
          p2 = target.find('.b-p2');
          p3 = target.find('.b-p3');
          p4 = target.find('.b-p4');
          pNwrap = pN.find('.b-wrap');
          p0wrap = p0.find('.b-wrap');
          p1wrap = p1.find('.b-wrap');
          p2wrap = p2.find('.b-wrap');
          p3wrap = p3.find('.b-wrap');
          p4wrap = p4.find('.b-wrap');
          wraps = target.find('.b-wrap');
        ***REMOVED***,
        updatePageCSS = function () ***REMOVED***
          wraps.css(css.wrap);
          p0wrap.css(css.p0wrap);
          p1.css(css.p1);
          p2.css(css.p2);
          pN.css(css.pN);
          p0.css(css.p0);
          p3.stop().css(css.p3);
          p4.css(css.p4);

          target.width(options.width);
        ***REMOVED***,
        destroyPages = function () ***REMOVED***
          var bWrap = target.find('.b-wrap');

          // remove booklet markup
          bWrap.unwrap();
          bWrap.children().unwrap();
          target.find('.b-counter, .b-page-blank, .b-page-empty').remove();
        ***REMOVED***,
        setWidthAndHeight = function() ***REMOVED***
          var parent = target.parent(),
              OpWidth = options.width,
              OpHeight = options.height;

          // Set width.
          if (OpWidth && typeof OpWidth === 'string') ***REMOVED***
            if (OpWidth.indexOf('px') !== -1) ***REMOVED***
              options.width = OpWidth.replace('px', '');
            ***REMOVED*** else if (OpWidth.indexOf('%') !== -1) ***REMOVED***
              wPercent = true;
              wOrig = OpWidth;
              options.width = parseFloat((OpWidth.replace('%', '') / 100) * parent.width());
            ***REMOVED***
          ***REMOVED***

          // Set height.
          if (OpHeight && typeof OpHeight === 'string' && OpHeight !== '100%') ***REMOVED***
            if (OpHeight.indexOf('px') !== -1) ***REMOVED***
              options.height = OpHeight.replace('px', '');
            ***REMOVED*** else if (OpHeight.indexOf('%') !== -1) ***REMOVED***
              hPercent = true;
              hOrig = OpHeight;
              options.height = parseFloat((OpHeight.replace('%', '') / 100) * parent.height());
            ***REMOVED***
          ***REMOVED***

          // save page sizes and other vars
          pWidth = options.width / 2;
          pWidthN = '-' + pWidth + 'px';
          pWidthH = pWidth / 2;
          pHeight = options.height;
        ***REMOVED***,
        updateOptions = function(newOptions) ***REMOVED***
          var didUpdate = false;
          var targetWidth = 0;
          var targetHeight = 0;

          // update options if newOptions have been passed in
          if (newOptions !== null && newOptions !== undefined) ***REMOVED***
            // remove page structure, revert to original order
            destroyPages();
            destroyControls();
            options = $.extend(***REMOVED******REMOVED***, options, newOptions);
            didUpdate = true;
            initPages();
          ***REMOVED***

          setWidthAndHeight();

          speedH = options.speed / 2;

          // set total page count
          options.pageTotal = target.children('.b-page').length;

          // update all CSS, as sizes may have changed
          updateCSSandAnimations();
          if (isInit) ***REMOVED***
            updatePages();
          ***REMOVED***

          // percentage resizing
          target.on('resize', function() ***REMOVED***
            var $target = $(target);
            var w = $target.width();
            var h = $target.height();

            if (options.autoSize && options.$containerW && options.$containerH) ***REMOVED***
              if (targetWidth !== w || targetHeight !== h) ***REMOVED***
                targetWidth = w;
                targetHeight = h;
                updateSize();
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***);

          isPlaying = false;

          // if options were updated force pages, controls and menu to update
          if (didUpdate) ***REMOVED***
            updatePages();
          ***REMOVED***
        ***REMOVED***,
        updateCSSandAnimations = function() ***REMOVED***
          // init base css
          css = ***REMOVED***
            'wrap': ***REMOVED***
              'left': 0,
              'width': pWidth - (options.pagePadding * 2),
              //'height': pHeight - (options.pagePadding * 2),
              'height': pHeight,
              'padding': options.pagePadding,
              'overflow-y': 'auto',
              'opacity': 1
            ***REMOVED***,
            'p0wrap': ***REMOVED***
              'right': 0,
              'left': 'auto'
            ***REMOVED***,
            'p1': ***REMOVED***
              'left': 0,
              'width': pWidth,
              'height': pHeight
            ***REMOVED***,
            'p2': ***REMOVED***
              'left': pWidth - 20,
              'width': pWidth,
              'opacity': 1,
              'height': pHeight
            ***REMOVED***,
            'pN': ***REMOVED***
              'left': 0,
              'width': pWidth,
              'height': pHeight
            ***REMOVED***,
            'p0': ***REMOVED***
              'left': 0,
              'width': 0,
              'height': pHeight
            ***REMOVED***,
            'p3': ***REMOVED***
              'left': pWidth * 2,
              'width': 0,
              'height': pHeight,
              'padding-left': 0
            ***REMOVED***,
            'p4': ***REMOVED***
              'left': pWidth - 20,
              'width': pWidth,
              'height': pHeight
            ***REMOVED***,
            'pwrap': ***REMOVED***
              'hover': ***REMOVED***
                'opacity': 0.1,
                'overflow-y': 'hidden'
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***;

          hoverShadowWidth = 10;
          hoverFullWidth = options.hoverWidth + hoverShadowWidth;
          hoverCurlWidth = (options.hoverWidth / 2) + hoverShadowWidth;

          // init animation params
          anim = ***REMOVED***
            'hover': ***REMOVED***
              'speed': options.hoverSpeed,
              'size': options.hoverWidth,
              'p2': ***REMOVED***
                'width': pWidth - hoverCurlWidth
              ***REMOVED***,
              'p3': ***REMOVED***
                'left': options.width - hoverFullWidth,
                'width': hoverCurlWidth
              ***REMOVED***,
              'p3closed': ***REMOVED***
                'left': pWidth - options.hoverWidth,
                'width': hoverCurlWidth
              ***REMOVED***,
              'p3wrap': ***REMOVED***
                'left': hoverShadowWidth
              ***REMOVED***,
              'p2end': ***REMOVED***
                'width': pWidth
              ***REMOVED***,
              'p2closedEnd': ***REMOVED***
                'width': pWidth,
                'left': 0
              ***REMOVED***,
              'p3end': ***REMOVED***
                'left': options.width,
                'width': 0
              ***REMOVED***,
              'p3closedEnd': ***REMOVED***
                'left': pWidth,
                'width': 0
              ***REMOVED***,
              'p3wrapEnd': ***REMOVED***
                'left': 10
              ***REMOVED***,
              'p1': ***REMOVED***
                'left': hoverCurlWidth,
                'width': pWidth - hoverCurlWidth
              ***REMOVED***,
              'p1wrap': ***REMOVED***
                'left': '-' + hoverCurlWidth + 'px'
              ***REMOVED***,
              'p0': ***REMOVED***
                'left': hoverCurlWidth,
                'width': hoverCurlWidth
              ***REMOVED***,
              'p0wrap': ***REMOVED***
                'right': hoverShadowWidth
              ***REMOVED***,
              'p1end': ***REMOVED***
                'left': 0,
                'width': pWidth
              ***REMOVED***,
              'p1wrapEnd': ***REMOVED***
                'left': 0
              ***REMOVED***,
              'p0end': ***REMOVED***
                'left': 0,
                'width': 0
              ***REMOVED***,
              'p0wrapEnd': ***REMOVED***
                'right': 0
              ***REMOVED***
            ***REMOVED***,
            // Forward.
            'p2': ***REMOVED***
              'width': 0
            ***REMOVED***,
            'p2closed': ***REMOVED***
              'width': 0,
              'left': pWidth
            ***REMOVED***,
            'p4closed': ***REMOVED***
              'left': pWidth
            ***REMOVED***,
            'p3in': ***REMOVED***
              'left': pWidthH,
              'width': pWidthH,
              'padding-left': options.shadowBtmWidth
            ***REMOVED***,
            'p3inDrag': ***REMOVED***
              'left': pWidth / 4,
              'width': pWidth * 0.75,
              'padding-left': options.shadowBtmWidth
            ***REMOVED***,
            'p3out': ***REMOVED***
              'left': 0,
              'width': pWidth,
              'padding-left': 0
            ***REMOVED***,
            'p3wrapIn': ***REMOVED***
              'left': options.shadowBtmWidth
            ***REMOVED***,
            'p3wrapOut': ***REMOVED***
              'left': 0
            ***REMOVED***,
            // Backwards.
            'p1': ***REMOVED***
              'left': pWidth,
              'width': 0
            ***REMOVED***,
            'p1wrap': ***REMOVED***
              'left': pWidthN
            ***REMOVED***,
            'p0': ***REMOVED***
              'left': pWidth,
              'width': pWidth
            ***REMOVED***,
            'p0in': ***REMOVED***
              'left': pWidthH,
              'width': pWidthH
            ***REMOVED***,
            'p0out': ***REMOVED***
              'left': pWidth,
              'width': pWidth
            ***REMOVED***,
            'p0outClosed': ***REMOVED***
              'left': 0,
              'width': pWidth
            ***REMOVED***,
            'p2back': ***REMOVED***
              'left': 0
            ***REMOVED***,
            'p0wrapDrag': ***REMOVED***
              'right': 0
            ***REMOVED***,
            'p0wrapIn': ***REMOVED***
              'right': options.shadowBtmWidth
            ***REMOVED***,
            'p0wrapOut': ***REMOVED***
              'right': 0
            ***REMOVED***
          ***REMOVED***;
        ***REMOVED***,
        updateSize = function () ***REMOVED***
          var height = options.$containerH.outerHeight(true),
              width = options.$containerW.outerWidth(true);

          if (target.hasClass('booklet')) ***REMOVED***
            options.width = width + 'px';
            if (options.height !== '100%') ***REMOVED***
              options.height = height + 'px';
            ***REMOVED***

            setWidthAndHeight();
            updateCSSandAnimations();
            updatePageCSS();
          ***REMOVED***
        ***REMOVED***,
        updateManualControls = function () ***REMOVED***
          var origX, newX, diff, fullPercent, shadowPercent, shadowW, curlW, 
              underW, curlLeft, p1wrapLeft, bPage = target.find('.b-page');
          isHoveringRight = isHoveringLeft = p3drag = p0drag = false;

          if ($.ui && options.manual) ***REMOVED***
            // manual page turning, check if jQuery UI is loaded
            if (bPage.draggable()) ***REMOVED***
              bPage.draggable('destroy').removeClass('b-grab b-grabbing');
            ***REMOVED***

            // implement draggable forward
            p3.draggable(***REMOVED***
              axis: 'x',
              containment: [
                target.offset().left, 0,
                (p2.offset() !== undefined ? p2.offset().left : 0) + pWidth - hoverFullWidth,
                pHeight
              ],
              drag: function (event, ui) ***REMOVED***
                p3drag = true;
                p3.removeClass('b-grab').addClass('b-grabbing');

                // calculate positions
                origX = ui.originalPosition.left;
                newX = ui.position.left;
                diff = origX - newX;
                fullPercent = diff / origX;
                shadowPercent = fullPercent < 0.5 ? fullPercent : (1 - fullPercent);
                shadowW = (shadowPercent * options.shadowBtmWidth * 2) + hoverShadowWidth;
                shadowW = diff / origX >= 0.5 ? shadowW -= hoverShadowWidth : shadowW;

                // set top page curl width
                curlW = hoverCurlWidth + diff / 2;
                curlW = curlW > pWidth ? pWidth : curlW; // constrain max width
                // set bottom page width, hide
                underW = pWidth - curlW;

                // set values
                p3.width(curlW);
                p3wrap.css(***REMOVED***
                  'left': shadowW
                ***REMOVED***);
                p2.width(underW);
              ***REMOVED***,
              stop: function () ***REMOVED***
                endHoverAnimation(false);
                if (fullPercent > options.hoverThreshold) ***REMOVED***
                  next();
                  p3.removeClass('b-grab b-grabbing');
                ***REMOVED*** else ***REMOVED***
                  p3drag = false;
                  p3.removeClass('b-grabbing').addClass('b-grab');
                ***REMOVED***
              ***REMOVED***
            ***REMOVED***);

            // implement draggable backwards
            p0.draggable(***REMOVED***
              'axis': 'x',
              //containment: 'parent',
              'containment': [
                target.offset().left + hoverCurlWidth,
                0,
                target.offset().left + options.width,
                pHeight
              ],
              'drag': function (event, ui) ***REMOVED***
                p0drag = true;
                p0.removeClass('b-grab').addClass('b-grabbing');

                // calculate positions
                origX = ui.originalPosition.left;
                newX = ui.position.left;
                diff = newX - origX;
                fullPercent = diff / (options.width - origX);
                if (fullPercent > 1) ***REMOVED***
                    fullPercent = 1;
                ***REMOVED***

                shadowPercent = fullPercent < 0.5 ? fullPercent : (1 - fullPercent);
                shadowW = (shadowPercent * options.shadowBtmWidth * 2) + hoverShadowWidth;
                shadowW = diff / origX >= 0.5 ? shadowW -= hoverShadowWidth : shadowW;

                curlW = fullPercent * (pWidth - hoverCurlWidth) + hoverCurlWidth + shadowW;
                curlLeft = curlW - shadowW;
                p1wrapLeft = -curlLeft;

                // set values
                ui.position.left = curlLeft;
                p0.css(***REMOVED***width: curlW***REMOVED***);
                p0wrap.css(***REMOVED***right: shadowW***REMOVED***);
                p1.css(***REMOVED***left: curlLeft, width: pWidth - curlLeft***REMOVED***);
                p1wrap.css(***REMOVED***left: p1wrapLeft***REMOVED***);
              ***REMOVED***,
              'stop': function () ***REMOVED***
                endHoverAnimation(true);
                if (fullPercent > options.hoverThreshold) ***REMOVED***
                  prev();
                  p0.removeClass('b-grab b-grabbing');
                ***REMOVED*** else ***REMOVED***
                  p0drag = false;
                  p0.removeClass('b-grabbing').addClass('b-grab');
                ***REMOVED***
              ***REMOVED***
            ***REMOVED***);

            bPage.off('click.booklet');

            if (options.hoverClick) ***REMOVED***
              target.find('.b-pN, .b-p0').on('click.booklet', prev).css(***REMOVED***cursor: 'pointer'***REMOVED***);
              target.find('.b-p3, .b-p4').on('click.booklet', next).css(***REMOVED***cursor: 'pointer'***REMOVED***);
            ***REMOVED***

            // mouse tracking for page movement
            target.off('mousemove.booklet').on('mousemove.booklet', function (e) ***REMOVED***
              diff = e.pageX - target.offset().left;
              diff += e.pageX > 300 ? options.scrollWidth : options.scrollWidth*-1;
              if (diff < anim.hover.size) ***REMOVED***
                startHoverAnimation(false);
              ***REMOVED*** else if (diff > anim.hover.size && diff <= options.width - anim.hover.size) ***REMOVED***
                endHoverAnimation(false);
                endHoverAnimation(true);
              ***REMOVED*** else if (diff > options.width - anim.hover.size) ***REMOVED***
                startHoverAnimation(true);
              ***REMOVED***
            ***REMOVED***).off('mouseleave.booklet').on('mouseleave.booklet', function () ***REMOVED***
              endHoverAnimation(false);
              endHoverAnimation(true);
            ***REMOVED***);
          ***REMOVED*** else ***REMOVED***
            bPage.off('click.booklet');
            
            target.find('.b-p1').on('click.booklet', function(event) ***REMOVED***
              event.preventDefault();
              prev();
            ***REMOVED***);
            target.find('.b-p2').on('click.booklet', function(event) ***REMOVED***
              event.preventDefault();
              next();
            ***REMOVED***);
          ***REMOVED***
        ***REMOVED***,
        destroyControls = function () ***REMOVED***
          destroyManualControls();
        ***REMOVED***,
        destroyManualControls = function () ***REMOVED***
          var bPage = target.find('.b-page');
          if ($.ui) ***REMOVED***
            // remove old draggables
            if (bPage.draggable()) ***REMOVED***
              bPage.draggable('destroy').removeClass('b-grab b-grabbing');
            ***REMOVED***
          ***REMOVED***
          // remove mouse tracking for page movement
          target.off('.booklet');
        ***REMOVED***,

        /* -------------------- Pages -------------------- */

        addPage = function (index, html) ***REMOVED***
          // validate inputs
          if (index === 'first') ***REMOVED***
            index = 0;
          ***REMOVED*** else if (index === 'last') ***REMOVED***
            index = originalPageTotal;
          ***REMOVED*** else if (typeof index === 'number') ***REMOVED***
            if (index < 0 || index > originalPageTotal) ***REMOVED***
              return;
            ***REMOVED***
          ***REMOVED*** else if (index === undefined) ***REMOVED***
            return;
          ***REMOVED***

          if (html === undefined || html === '') ***REMOVED***
            return;
          ***REMOVED***

          // remove page structure, revert to original order
          destroyPages();
          destroyControls();

          // add new page
          if (index === originalPageTotal) ***REMOVED***
            //end of book
            target.children(':eq(' + (index - 1) + ')').after(html);
          ***REMOVED*** else ***REMOVED***
            target.children(':eq(' + index + ')').before(html);
          ***REMOVED***

          originalPageTotal = target.children().length;

          // recall initialize functions
          initPages();
          updateOptions();
          updatePages();
        ***REMOVED***,
        removePage = function (index) ***REMOVED***
          var removedPage;

          // validate inputs
          if (index === 'start') ***REMOVED***
            index = 0;
          ***REMOVED*** else if (index === 'end') ***REMOVED***
            index = originalPageTotal;
          ***REMOVED*** else if (typeof index === 'number') ***REMOVED***
            if (index < 0 || index > originalPageTotal) ***REMOVED***
              return;
            ***REMOVED***
          ***REMOVED*** else if (index === undefined) ***REMOVED***
            return;
          ***REMOVED***

          // stop if removing last remaining page
          if (target.children('.b-page').length === 2 && target.find('.b-page-blank').length > 0) ***REMOVED***
            return;
          ***REMOVED***

          // remove page structure, revert to original order
          destroyPages();
          destroyControls();

          if (index >= options.currentIndex) ***REMOVED***
            if (index > 0 && (index % 2) !== 0) ***REMOVED***
              options.currentIndex -= 2;
            ***REMOVED***
            if (options.currentIndex < 0) ***REMOVED***
              options.currentIndex = 0;
            ***REMOVED***
          ***REMOVED***

          // remove page
          if (index === originalPageTotal) ***REMOVED***
            // end of book
            removedPage = target.children(':eq(' + (index - 1) + ')').remove();
          ***REMOVED*** else ***REMOVED***
            removedPage = target.children(':eq(' + index + ')').remove();
          ***REMOVED***

          originalPageTotal = target.children().length;

          removedPage = null;

          // recall initialize functions
          initPages();
          updatePages();
          updateOptions();
        ***REMOVED***,

        /* -------------------- Navigation -------------------- */

        next = function () ***REMOVED***
          var index;

          if (!isBusy) ***REMOVED***
            if (isPlaying && options.currentIndex + 2 >= options.pageTotal) ***REMOVED***
              index = options.pageTotal - 1;
            ***REMOVED*** else ***REMOVED***
              index = options.currentIndex + 2;
            ***REMOVED***
          ***REMOVED***
          goToPage(index);
          options.onGotoPage(index);
        ***REMOVED***,
        prev = function () ***REMOVED***
          var index;

          if (!isBusy) ***REMOVED***
            if (isPlaying && options.currentIndex - 2 < 0) ***REMOVED***
              index = 0;
            ***REMOVED*** else ***REMOVED***
              index = options.currentIndex - 2;
            ***REMOVED***
          ***REMOVED***
          goToPage(index);
          options.onGotoPage(index);
        ***REMOVED***,
        animations = ***REMOVED***
          leaf: function(newIndex) ***REMOVED***
            var speed;

            // moving forward (increasing number)
            if (newIndex > options.currentIndex) ***REMOVED***
              diff = newIndex - options.currentIndex;

              // set animation speed, depending if user dragged any distance or not
              speed = p3drag === true ? options.speed * (p3.width() / pWidth) : speedH;

              startPageAnimation(diff, true, speed);

              // hide p2 as p3 moves across it
              p2.stop().animate(anim.p2, speed, p3drag === true ? options.easeOut : options.easeIn);

              // if animating after a manual drag, calculate new speed and animate out
              if (p3drag) ***REMOVED***
                p3.animate(anim.p3out, speed, options.easeOut);
                p3wrap.animate(anim.p3wrapOut, speed, options.easeOut, function() ***REMOVED***
                  updateAfter();
                ***REMOVED***);
              ***REMOVED*** else ***REMOVED***
                p3.stop()
                  .animate(anim.p3in, speed, options.easeIn)
                  .animate(anim.p3out, speed, options.easeOut);
                p3wrap
                  .animate(anim.p3wrapIn, speed, options.easeIn)
                  .animate(anim.p3wrapOut, speed, options.easeOut, function() ***REMOVED***
                    updateAfter();
                  ***REMOVED***);
              ***REMOVED***
            ***REMOVED*** else if (newIndex < options.currentIndex) ***REMOVED***
              // moving backward (decreasing number)
              diff = options.currentIndex - newIndex;

              // set animation speed, depending if user dragged any distance or not
              speed = p0drag === true ? options.speed * (p0.width() / pWidth) : speedH;
              startPageAnimation(diff, false, speed);

              if (p0drag) ***REMOVED***
                // hide p1 as p0 moves across it
                p1.animate(anim.p1, speed, options.easeOut);
                p1wrap.animate(anim.p1wrap, speed, options.easeOut);
                p0.animate(anim.p0, speed, options.easeOut);

                p0wrap.animate(anim.p0wrapDrag, speed, options.easeOut, function() ***REMOVED***
                  updateAfter();
                ***REMOVED***);
              ***REMOVED*** else ***REMOVED***
                // hide p1 as p0 moves across it
                p1.animate(anim.p1, speed * 2, options.easing);
                p1wrap.animate(anim.p1wrap, speed * 2, options.easing);

                p0
                  .animate(anim.p0in, speed, options.easeIn)
                  .animate(anim.p0out, speed, options.easeOut);

                p0wrap
                  .animate(anim.p0wrapIn, speed, options.easeIn)
                  .animate(anim.p0wrapOut, speed, options.easeOut, function() ***REMOVED***
                    updateAfter();
                  ***REMOVED***);
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***,
          flip: function(newIndex) ***REMOVED***
            var speed = 'fast';
            var tmp;

            if (newIndex > options.currentIndex) ***REMOVED***
              // NEXT
              diff = newIndex - options.currentIndex;
              startPageAnimation(diff, true, speed);
              tmp = $('<div>').css(***REMOVED***
                      'width': 1 + 'px',
                      'position': 'absolute',
                      'height': target.height() + 'px',
                      'left': parseInt(p2.css('left'), 10) + 'px',
                      'top': 0,
                      'z-index': 21,
                      'border': '1px solid #ccc',
                      'padding': 0
                    ***REMOVED***)
                    .appendTo(target);

              p2.stop().animate(***REMOVED***
                width: 0
              ***REMOVED***, speed, options.easeIn, function() ***REMOVED***
                tmp.stop().animate(***REMOVED***
                  left: 0
                ***REMOVED***, speed, options.easeIn, function() ***REMOVED***
                  tmp.remove();
                ***REMOVED***);

                p3.css(anim.p3out);
                p3wrap.css(anim.p3wrapOut);
                updateAfter();
              ***REMOVED***);
            ***REMOVED*** else if (newIndex < options.currentIndex) ***REMOVED***
              //speed = 2000;
              diff = options.currentIndex - newIndex;
              startPageAnimation(diff, false, speed);

              tmp = $('<div>').css(***REMOVED***
                      'width': 1 + 'px',
                      'position': 'absolute',
                      'height': target.height() + 'px',
                      'left': 0,
                      'top': 0,
                      'z-index': 21,
                      'border': '1px solid #ccc',
                      'padding': 0
                    ***REMOVED***)
                    .appendTo(target);

              p1.animate(anim.p1, speed, options.easing);
              tmp.stop().animate(***REMOVED***
                  left: anim.p0in.left * 2
                ***REMOVED***, speed, options.easing, function() ***REMOVED***
                  tmp.remove();
                ***REMOVED***);
              p1wrap.animate(anim.p1wrap, speed, options.easeIn, function() ***REMOVED***                
                p0.css(***REMOVED***
                  'left': anim.p0in.left * 2 - 20 + 'px',
                  'overflow-y': 'hidden'
                ***REMOVED***);
                p0.animate(***REMOVED***
                  width: anim.p0in.width * 2 - 20 + 'px'
                ***REMOVED***, speed, options.easeIn, function() ***REMOVED***
                  p0.css(***REMOVED***
                    'overflow-y': 'auto'
                  ***REMOVED***);
                  p0wrap.css(anim.p0wrapOut);
                  updateAfter();
                ***REMOVED***);
              ***REMOVED***);
            ***REMOVED***
          ***REMOVED***
        ***REMOVED***,
        animation = function(newIndex, type) ***REMOVED***
          animations[type || options.animation](newIndex);
        ***REMOVED***,
        goToPage = function (newIndex, manualSwitch) ***REMOVED***
          manualSwitch = manualSwitch || false;

          if (newIndex < options.pageTotal && newIndex >= 0 && !isBusy) ***REMOVED***
            if (!manualSwitch) ***REMOVED***
              isBusy = true;
            ***REMOVED***
            animation(newIndex);
            options.currentIndex = newIndex;
          ***REMOVED***
        ***REMOVED***,
        startHoverAnimation = function (inc) ***REMOVED***
          var p2Width = p2wrap.width();

          if (options.hovers || options.manual) ***REMOVED***
            if (inc) ***REMOVED***
              if (!isBusy && !isHoveringRight && !isHoveringLeft && !p3drag && options.currentIndex + 2 <= options.pageTotal - 1) ***REMOVED***
                p2.stop().animate(anim.hover.p2, anim.hover.speed, options.easing);
                p3.addClass('b-grab');
                p3.stop().animate(anim.hover.p3, anim.hover.speed, options.easing);
                p3wrap.stop().animate(anim.hover.p3wrap, anim.hover.speed, options.easing);
                isHoveringRight = true;
                p2wrap.data('widthBeforeHover', p2Width);
                p2wrap.width(p2Width - anim.hover.p3.width);
                p4wrap.css(css.pwrap.hover);
              ***REMOVED***
            ***REMOVED*** else ***REMOVED***
              if (!isBusy && !isHoveringLeft && !isHoveringRight && !p0drag && options.currentIndex - 2 >= 0) ***REMOVED***
                p1.stop().animate(anim.hover.p1, anim.hover.speed, options.easing);
                p0.addClass('b-grab');
                p1wrap.stop().animate(anim.hover.p1wrap, anim.hover.speed, options.easing);
                p0.stop().animate(anim.hover.p0, anim.hover.speed, options.easing);
                p0wrap.stop().animate(anim.hover.p0wrap, anim.hover.speed, options.easing);
                isHoveringLeft = true;
                p0wrap.css(***REMOVED***
                  'overflow-y': 'hidden'
                ***REMOVED***);
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***
        ***REMOVED***,
        endHoverAnimation = function (inc) ***REMOVED***
          if (options.hovers || options.manual) ***REMOVED***
            if (inc) ***REMOVED***
              if (!isBusy && isHoveringRight && !p3drag && options.currentIndex + 2 <= options.pageTotal - 1) ***REMOVED***
                p2.stop().animate(anim.hover.p2end, anim.hover.speed, options.easing);
                p3.stop().animate(anim.hover.p3end, anim.hover.speed, options.easing);
                p3wrap.stop().animate(anim.hover.p3wrapEnd, anim.hover.speed, options.easing);
                p2wrap.width(p2wrap.data('widthBeforeHover'));
                p4wrap.css(css.wrap);
                isHoveringRight = false;
              ***REMOVED***
            ***REMOVED*** else ***REMOVED***
              if (!isBusy && isHoveringLeft && !p0drag && options.currentIndex - 2 >= 0) ***REMOVED***
                p1.stop().animate(anim.hover.p1end, anim.hover.speed, options.easing);
                p1wrap.stop().animate(anim.hover.p1wrapEnd, anim.hover.speed, options.easing);
                p0.stop().animate(anim.hover.p0end, anim.hover.speed, options.easing);
                p0wrap.stop().animate(anim.hover.p0wrapEnd, anim.hover.speed, options.easing);
                p0wrap.css(css.wrap);
                isHoveringLeft = false;
              ***REMOVED***
            ***REMOVED***
          ***REMOVED***
        ***REMOVED***,
        startPageAnimation = function (diff, inc) ***REMOVED***
            var currIndex = options.currentIndex;

            // setup content
            if (inc && diff > 2) ***REMOVED***
              // initialize next 2 pages, if jumping forward in the book
              target.find('.b-p3, .b-p4').removeClass('b-p3 b-p4').hide();
              target.find('.b-page-' + currIndex).addClass('b-p3').show().stop().css(css.p3);
              target.find('.b-page-' + (currIndex + 1)).addClass('b-p4').show().css(css.p4);
              target.find('.b-page-' + currIndex + ' .b-wrap').show().css(css.wrap);
              target.find('.b-page-' + (currIndex + 1) + ' .b-wrap').show().css(css.wrap);

              if (isHoveringRight) ***REMOVED***
                p3.css(***REMOVED***
                  'left': options.width - 40,
                  'width': 20,
                  'padding-left': 10
                ***REMOVED***);
              ***REMOVED***
            ***REMOVED*** else if (!inc && diff > 2) ***REMOVED***
              // initialize previous 2 pages, if jumping backwards in the book
              target.find('.b-pN, .b-p0').removeClass('b-pN b-p0').hide();
              target.find('.b-page-' + currIndex).addClass('b-pN').show().css(css.pN);
              target.find('.b-page-' + (currIndex + 1)).addClass('b-p0').show().css(css.p0);
              target.find('.b-page-' + currIndex + ' .b-wrap').show().css(css.wrap);
              target.find('.b-page-' + (currIndex + 1) + ' .b-wrap').show().css(css.wrap);
              p0wrap.css(css.p0wrap);

              if (isHoveringLeft) ***REMOVED***
                p0.css(***REMOVED***
                  left: 10,
                  width: 40
                ***REMOVED***);
                p0wrap.css(***REMOVED***
                  right: 10
                ***REMOVED***);
              ***REMOVED***
            ***REMOVED***
        ***REMOVED***,
        updateAfter = function () ***REMOVED***
          updatePages();
          isBusy = false;
        ***REMOVED***;

    /* -------------------------- API -------------------------- */

    return ***REMOVED***
      init: init,
      destroy: destroy,
      next: next,
      prev: prev,
      gotopage: function (index) ***REMOVED***
        // validate inputs
        if (typeof index === 'string') ***REMOVED***
          if (index === 'first') ***REMOVED***
            index = 0;
          ***REMOVED*** else if (index === 'last') ***REMOVED***
            index = options.pageTotal - 1;
          ***REMOVED*** else ***REMOVED***
            this.gotopage(parseInt(index));
          ***REMOVED***
        ***REMOVED*** else if (typeof index === 'number') ***REMOVED***
          if (index < 0 || index >= options.pageTotal) ***REMOVED***
            return;
          ***REMOVED***
        ***REMOVED*** else if (index === undefined) ***REMOVED***
          return;
        ***REMOVED***

        // adjust for odd page
        if (index % 2 !== 0) ***REMOVED***
          index -= 1;
        ***REMOVED***

        goToPage(index, true);
      ***REMOVED***,
      add: addPage,
      remove: removePage,
      option: function (name, value) ***REMOVED***
        if (typeof name === 'string') ***REMOVED***
          // if option exists
          if (options[name] !== undefined) ***REMOVED***
            if (value !== undefined) ***REMOVED***
              // if value is sent in, set the option value and update options
              options[name] = value;
              updateOptions();
            ***REMOVED*** else ***REMOVED***
              // if no value sent in, get the current option value
              return options[name];
            ***REMOVED***
          ***REMOVED*** else ***REMOVED***
            $.error('Option "' + name + '" does not exist on jQuery.booklet.');
          ***REMOVED***
        ***REMOVED*** else if (typeof name === 'object') ***REMOVED***
          // if sending in an object, update options
          updateOptions(name);
        ***REMOVED*** else if (name === undefined || !name) ***REMOVED***
          // return a copy of the options object, to avoid changes
          return $.extend(***REMOVED******REMOVED***, options);
        ***REMOVED***
      ***REMOVED***
    ***REMOVED***;
  ***REMOVED***

  // define default options
  $.fn.booklet.defaults = ***REMOVED***
    width: 600, // container width, px
    height: 400, // container height, px
    speed: 1000, // speed of the transition between pages
    startingPage: 0, // index of the first page to be displayed
    autoSize: false,
    $containerW: null,
    $containerH: null,
    animation: 'leaf', // flip || leaf
    onGotoPage: $.noop,
    easing: 'easeInOutQuad', // easing method for complete transition
    easeIn: 'easeInQuad', // easing method for first half of transition
    easeOut: 'easeOutQuad', // easing method for second half of transition
    pagePadding: 10, // padding for each page wrapper
    manual: true, // enables manual page turning, requires jQuery UI to function
    hovers: true, // enables preview page-turn hover animation, shows a small preview of previous or next page on hover
    hoverWidth: 50, // default width for page-turn hover preview
    hoverSpeed: 500, // default speed for page-turn hover preview
    hoverThreshold: 0.25, // default percentage used for manual page dragging, sets the percentage amount a drag must be before moving next or prev
    hoverClick: true, // enables hovered arreas to be clicked when using manual page turning
    scrollWidth: 30,
    shadowBtmWidth: 30 // shadow width for bottom shadow
  ***REMOVED***;
***REMOVED***)(this, jQuery);
