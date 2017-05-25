(function() {
    angular.module('Home', []);
    angular.module('Home').filter('dateFilter', function() {
        return function(input) {
            var date;
            date = moment(input).utcOffset('+0000').format("MMMM Do YYYY, h:mm:ss");
            return date;
        };
    });
})();