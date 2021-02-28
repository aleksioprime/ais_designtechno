new Vue({
    el: '#sumassess',
    data: {
        objective: [],
        criteria: [],
        year_ib: [],
        currentObj: {
            'A': [],
            'B': [],
            'C': [],
            'D': [],
        },
        currentObjA: [],
        currentObjB: [],
        currentObjC: [],
        currentObjD: [],
    },
    created: function () {
        const vm = this;
        axios.get('/api/criteria')
            .then(function (response) {
                vm.criteria = response.data
                console.log('Критерии: ', vm.criteria)
            })
        axios.get('/api/yearib')
            .then(function (response) {
                vm.year_ib = response.data
                console.log('Года обучения: ', vm.year_ib)
            })
        this.getObjective(1)
    },
    computed: {
    },
    methods: {
        async getObjective(year_ib) {
            this.currentObj = await axios.get('/api/objective', {
                params: {
                    'year': year_ib
                }
            }).then(function (response) {
                currentObjA = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'A';
                });
                currentObjB = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'B';
                });
                currentObjC = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'C';
                });
                currentObjD = response.data.filter(function (obj) {
                    return obj.criteria.letter == 'D';
                });
                return {'A': currentObjA, 'B': currentObjB, 'C': currentObjC, 'D': currentObjD}
            })
            console.log(this.currentObj['A'])
        }
    }
})