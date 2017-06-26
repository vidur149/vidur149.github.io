angular.module('multifunctional', ['ui.router', 'angularMoment', 'vsGoogleAutocomplete']);
angular.module('multifunctional').config(function($stateProvider) {

    var index = {
        name: 'index',
        url: '',
        templateUrl: 'templates/home.html'
    };

    var stopwatch = {
        name: 'stopwatch',
        url: '/stopwatch',
        templateUrl: 'templates/stopwatch.html',
        controller: 'stopwatchController'
    };

    var todo = {
        name: 'todo',
        url: '/todo',
        templateUrl: 'templates/todo.html',
        controller: 'todoController'
    };

    var weather = {
        name: 'weather',
        url: '/weather',
        templateUrl: 'templates/weather.html',
        controller: 'weatherController'
    };

    $stateProvider.state(stopwatch);
    $stateProvider.state(todo);
    $stateProvider.state(weather);
    $stateProvider.state(index);
});


angular.module('multifunctional')
    .controller("stopwatchController", ['$scope', '$window', '$interval', function($scope, $window, $interval) {
        $scope.state = 'reset';

        $scope.time = function() {
            if ($window.localStorage.getItem('watchValue') == null) {
                $window.localStorage.setItem('watchValue', '00:00:00');
            }
            return $window.localStorage.getItem('watchValue');
        };

        $scope.startWatch = function() {
            $scope.state = 'start';
            $scope.watchValue = $scope.time();
            // Watch value is stored in hh:mm:ss format, 
            // hence we need to split it around ':' and then convert into hours,minutes and seconds
            var watchArray = $scope.watchValue.split(':');
            var hours = Number(watchArray[0]);
            var minutes = Number(watchArray[1]);
            var seconds = Number(watchArray[2]);
            // We have to increment the timer value every second, 
            // therefore we need to calculate the total seconds and then only we can 
            // increment the value by 1
            $scope.totalSeconds = hours * 3600 + minutes * 60 + seconds;

            if ($scope.myInterval) {
                $interval.cancel($scope.myInterval);
            }

            $scope.onInterval = function() {
                $scope.totalSeconds++;
                // after incrementing the value we need to convert it back into hh:mm:ss format                
                var hours = Math.floor($scope.totalSeconds / 3600);
                var minutes = Math.floor(($scope.totalSeconds - (hours * 3600)) / 60);
                var seconds = $scope.totalSeconds - (hours * 3600) - (minutes * 60);
                if (hours < 10) { hours = "0" + hours; }
                if (minutes < 10) { minutes = "0" + minutes; }
                if (seconds < 10) { seconds = "0" + seconds; }
                $scope.watchValue = hours + ':' + minutes + ':' + seconds;
                $window.localStorage.setItem('watchValue', $scope.watchValue);
            };

            $scope.myInterval = $interval($scope.onInterval, 100);

        };

        $scope.stopWatch = function() {
            $scope.state = 'stop';
            if ($scope.myInterval) {
                $interval.cancel($scope.myInterval);
            }
        };

        $scope.resetWatch = function() {
            $scope.stopWatch();
            $scope.state = 'reset';
            $window.localStorage.setItem('watchValue', '00:00:00');
        }
    }]);

angular.module("multifunctional").controller("todoController", myCtrl);
myCtrl.$inject = ['$http'];

function myCtrl($http) {
    var self = this;
    self.tasks = [{
            'title': 'Complete the Html Code',
            'id': 1,
            'createdDate': new Date(1498212323393)
        },
        {
            'title': 'Complete the JS code',
            'id': 2,
            'createdDate': new Date(1498212323399)
        }
    ];
    self.title;

    self.removeTask = function(id) {
        for (let i = 0; i < self.tasks.length; i++) {
            if (self.tasks[i]['id'] === id) {
                if (i > -1) {
                    self.tasks.splice(i, 1);
                }
                break;
            }
        }
    };

    self.addTask = function() {
        if (self.title !== "") {
            var len = self.tasks.length;
            var id;
            id = len === 0 ? 0 : self.tasks[len - 1]['id'] + 1;
            var task = {
                'title': self.title,
                'id': id,
                'createdDate': new Date()
            };
            self.tasks.push(task);
            self.title = '';
        }
    };
    self.order = '';
    self.orderByDate = function() {
        self.order = self.order == 'title' ? '' : 'title';
    };
}


angular.module('multifunctional')
    .controller("weatherController", ['$scope', '$http', function($scope, $http) {
        // get todays date and set the state according to hour of the day
        $scope.date = new Date();
        var hrs = $scope.date.getHours();
        // var hrs = $scope.data.getHours();
        var state = '';
        if (hrs > 6 && hrs < 20) {
            state = 'morning';
        } else if (hrs >= 20 & hrs <= 6) {
            state = 'night';
        }
        $scope.state = state;
        // get lat and lang of current position
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                $scope.lat = position.coords.latitude;
                $scope.long = position.coords.longitude;
                // get weather details of the current lat and long
                $scope.getWeather($scope.lat, $scope.long);
            });
        }

        $scope.getWeather = function(lat, long) {
            var api_key = '&appid=c745ee805737efda1aecd6d7545d8fe0&units=metric';
            var weather_endpoint = 'http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + long + api_key;

            $http.get(weather_endpoint).then(function(response) {
                $scope.response = response.data;
                $scope.img_src = "https://openweathermap.org/img/w/" + $scope.response.weather[0].icon + '.png';
                console.log($scope.response);
            });
        };
    }]);