odoo.define('export_pivot_to_pdf.PivotControllerPDF', function(require) {
    "use strict";
    var PivotController = require('web.PivotController');
    var rpc = require('web.rpc');


    PivotController.include({


        _downloadpdf:function(){
        var self = this;
        return rpc.query({
                    model: 'pivot.print',
                    method: 'call_pdf',
                    args: [$('.o_pivot ')[0].innerHTML,self.modelName,self.displayName],
                }).then(function(data){
                    return self.do_action(data);
                });

        },
        _updateButtons: function() {
            if (!this.$buttons) {
                return;
            }
            var self = this;
            var state = this.model.get({
                raw: true
            });
            _.each(this.measures, function(measure, name) {
                var isSelected = _.contains(state.measures, name);
                self.$buttons.find('.dropdown-item[data-field="' + name + '"]')
                    .toggleClass('selected', isSelected);
            });
            var noDataDisplayed = !state.hasData || !state.measures.length;
            this.$buttons.find('.o_pivot_flip_button').prop('disabled', noDataDisplayed);
            this.$buttons.find('.o_pivot_expand_button').prop('disabled', noDataDisplayed);
            this.$buttons.find('.o_pivot_download').prop('disabled', noDataDisplayed);
            this.$buttons.find('.o_pivot_download_pdf').prop('disabled', noDataDisplayed);
        },
        _onButtonClick: function(ev) {
            var $target = $(ev.target);
            if ($target.hasClass('o_pivot_flip_button')) {
                this.model.flip();
                this.update({}, {
                    reload: false
                });
            }
            if ($target.hasClass('o_pivot_expand_button')) {
                this.model.expandAll().then(this.update.bind(this, {}, {
                    reload: false
                }));
            }
            if (ev.target.closest('.o_pivot_measures_list')) {
                ev.preventDefault();
                ev.stopPropagation();
                const field = ev.target.dataset.field;
                if (field) {
                    this.model
                        .toggleMeasure(field)
                        .then(this.update.bind(this, {}, {
                            reload: false
                        }));
                }
            }
            if ($target.hasClass('o_pivot_download')) {
                this._downloadTable();
            }
             if ($target.hasClass('o_pivot_download_pdf')) {
                this._downloadpdf();
            }
        },

    });




});