const Criteria = {
    data() {
        return {
            isOpenCriteria: false,
            openCriteriaText: "Показать",
            isOpenSubjectGroup: false,
            openSubjectGroupText: 'Показать',
            programm: 2,
            subjectGroup: [],
            currentSubjectGroup: {},
            criteria: [],
            currentCriterion: {},
            strands: [],
            currentStrand: {},
            yearsIB: [],
            currentYear: {},
            objectives: [],
            levels: [],
            loading: false,
            data: false,
            extraData: false,
            extraLoading: false,
        }
    },
    computed: {
        accordionCriteria() {
            return {
                'is-closed': !this.isOpenCriteria,
            };
        },
        accordionSubjectGroup() {
            return {
                'is-closed': !this.isOpenSubjectGroup,
            };
        },
    },
    methods: {

        toggleAccordionCriteria() {
            this.isOpenCriteria = !this.isOpenCriteria;
            if (this.openCriteriaText == "Показать") {
                this.openCriteriaText = 'Скрыть'
            } else {
                this.openCriteriaText = 'Показать'
            }
            
        },

        toggleAccordionSubjectGroup() {
            this.isOpenSubjectGroup = !this.isOpenSubjectGroup;
            if (this.openSubjectGroupText == "Показать") {
                this.openSubjectGroupText = 'Скрыть'
            } else {
                this.openSubjectGroupText = 'Показать'
            }
        },

        async getSubjectsAndYearIB() {
            this.currentSubjectGroup = JSON.parse(document.getElementById('dataSubjectGroup').textContent);
            // Запрос на получение всех предметных групп выбранной программы IB
            this.subjectGroup = await axios.get('/api/sumassess/subjectgroups', {
                params: {
                    'programm': this.programm,
                }
            }).then(function (response) {
                console.log('Полученные предметы: ', response.data);
                return response.data;
            });
             // Запрос на получение всех лет обучения выбранной программы IB
             this.yearsIB = await axios.get('/api/sumassess/yearib', {
                params: {
                    'programm': this.programm,
                }
            }).then(function (response) {
                console.log('Полученные года обучения: ', response.data);
                return response.data;
            });
            this.currentYear = this.yearsIB[this.yearsIB.length - 1].id
            this.getObjectiveAndLevelByYear(this.currentYear)
        },

        async getCriteriaAndStrands(sg) {
            this.currentSubjectGroup = sg;
            console.log('Текущий предмет: ', sg);
            // Запрос на получение всех критериев выбранной предметной группы
            this.criteria = await axios.get('/api/sumassess/criteria', {
                params: {
                    'sg': this.currentSubjectGroup,
                }
            }).then(function (response) {
                console.log('Полученные критерии: ', response.data);
                return response.data;
            });
            // Запрос на получение всех стрендов выбранной предметной группы
            this.strands = await axios.get('/api/sumassess/strands', {
                params: {
                    'sg': this.currentSubjectGroup,
                }
            }).then(function (response) {
                console.log('Полученные стрэнды: ', response.data);
                return response.data;
            });
        },

        async getObjectiveAndLevelByYear(year) {
            this.currentYear = year;
            this.currentStrand = {};
            this.loading = true;
            this.data = false;
            console.log('Текущий год: ', year);
            // Запрос на получение всех образовательный целей выбранного года и критерия
            this.objectives = await axios.get('/api/sumassess/objectives', {
                params: {
                    'year': this.currentYear,
                }
            }).then(function (response) {
                console.log('Полученные образовательные цели: ', response.data);
                return response.data;
            });
            // Запрос на получение всех уровней достижений выбранного года и критерия
            this.levels = await axios.get('/api/sumassess/levels', {
                params: {
                    'year': this.currentYear,
                }
            }).then(function (response) {
                console.log('Полученные уровни достижений: ', response.data);
                return response.data;
            });
            this.loading = false;
            this.extraLoading = false;
            this.data = true;
            this.extraData = true;
            // window.scrollTo({
            //     top: 330,
            //     behavior: 'smooth'
            // });
        },

        getStrands(criterion) {
            return this.strands.filter(function (strand) {
                return strand.criteria.id == criterion
            });
        },

        getLevels(objective) {
            return this.levels.filter(function (level) {
                return level.objective.id == objective
            });
        },
        getSubjectGroup() {
            url = this.subjectGroup.find(sg => sg.id == this.currentSubjectGroup)
            console.log('Ссылка: ', url['schema']);
            return url
        }
    },
    mounted() {
        this.extraLoading = true;
        this.getSubjectsAndYearIB();
        if (this.currentSubjectGroup) {
            this.getCriteriaAndStrands(this.currentSubjectGroup)
        }
        
    },
}

Vue.createApp(Criteria).mount("#criteria")