(function() {
    angular.module("todo", []);
    angular.module("todo").controller("myCtrl", myCtrl);
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
})();