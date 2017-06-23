(function() {
    angular.module("todo", []);
    angular.module("todo").controller("myCtrl", myCtrl);
    myCtrl.$inject = ['$http'];

    function myCtrl($http) {
        var self = this;
        self.tasks = [{
                'title': 'Complete the Html Code',
                'id': 1
            },
            {
                'title': 'Complete the JS code',
                'id': 2
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
                    'id': id
                };
                self.tasks.push(task);
                self.title = '';
            }
        };
    }
})();