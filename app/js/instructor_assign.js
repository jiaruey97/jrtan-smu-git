const instructor_assign = new Vue({
                            el: '#app',
                            vuetify: new Vuetify(),
                            data: () => ({
                                dialog: false,
                                dialogDelete: false,
                                headers: [
                                {
                                    text: 'Courses',
                                    align: 'start',
                                    sortable: false,
                                    value: 'name',
                                },
                                { text: 'Duration', value: 'duration' },
                                { text: 'Details', value: 'details' },
                                { text: 'Instructor', value: 'instructor' },
                                { text: 'Actions', value: 'actions', sortable: false },
                                ],
                                courses: [],
                                editedIndex: -1,
                                editedItem: {
                                name: '',
                                duration: '',
                                details: '',
                                instructor:'',
                                },
                                defaultItem: {
                                name: '',
                                duration: '',
                                details: '',
                                instructor:'',
                                },
                            }),

                            computed: {
                                formTitle () {
                                return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
                                },
                            },

                            watch: {
                                dialog (val) {
                                val || this.close()
                                },
                                dialogDelete (val) {
                                val || this.closeDelete()
                                },
                            },

                            created () {
                                this.initialize()
                            },

                            methods: {
                                initialize () {
                                this.courses = [
                                    {
                                        name: 'On-Site Protocols',
                                        duration: '1.5 hours',
                                        details: 'This course gives you an overview of the.......................',
                                        instructor: 'Donald Trump',
                                    },
                                    {
                                        name: 'Installation',
                                        duration: '1 hour',
                                        details: 'This course gives you an overview of the.......................',
                                        instructor:'Richard Marx',
                                    },
                                    {
                                        name: 'Assembling',
                                        duration: '45 mins',
                                        details: 'This course gives you an overview of the.......................',
                                        instructor:'Collion Raye',
                                    },
                                ]
                                },

                                editItem (item) {
                                this.editedIndex = this.courses.indexOf(item)
                                this.editedItem = Object.assign({}, item)
                                this.dialog = true
                                },

                                deleteItem (item) {
                                this.editedIndex = this.courses.indexOf(item)
                                this.editedItem = Object.assign({}, item)
                                this.dialogDelete = true
                                },

                                deleteItemConfirm () {
                                this.courses.splice(this.editedIndex, 1)
                                this.closeDelete()
                                },

                                close () {
                                this.dialog = false
                                this.$nextTick(() => {
                                    this.editedItem = Object.assign({}, this.defaultItem)
                                    this.editedIndex = -1
                                })
                                },

                                closeDelete () {
                                this.dialogDelete = false
                                this.$nextTick(() => {
                                    this.editedItem = Object.assign({}, this.defaultItem)
                                    this.editedIndex = -1
                                })
                                },

                                save () {
                                if (this.editedIndex > -1) {
                                    Object.assign(this.courses[this.editedIndex], this.editedItem)
                                } else {
                                    this.courses.push(this.editedItem)
                                }
                                this.close()
                                },
                            },
                            })