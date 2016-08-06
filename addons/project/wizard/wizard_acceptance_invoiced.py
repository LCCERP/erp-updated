from lxml import etree
from openerp import tools
from openerp.tools.translate import _
from openerp.osv import fields, osv

class project_task_delegate_states(osv.osv_memory):
    
    def invoiced_tasks(self, cr, uid,ids, context=None):
        ids_list = []
        for rec in self.browse(cr, uid,ids):
            for idd in rec.project_taks_id:
                ids_list.append(idd.id)
            tasks_id = self.pool.get('project.task').search(cr, uid, [('id','in',ids_list),('state','=','Acceptance In Progress')], context=context)
            tasks_obj = self.pool.get('project.task').browse(cr, uid, tasks_id)
            
        for obj in tasks_obj:
            self.pool.get('project.task').write(cr,uid,obj.id,{'state':'Invoiced',
                                                               'needed_by_date':rec.needed_by_date,
                                                               'needed_by_date':rec.remarks,
                                                               'needed_by_date':rec.date_deadline,},context)
        return None
    
    _name = 'project.wizard.staterifts.invoiced'
    _description = 'Project State To Invoiced'
    _columns = {
        'project_taks_id':fields.many2many('project.task', 'project_task_state_acceptinvoiced_rel', 'task_id', 'parent_id',"Select Items"),
        'needed_by_date': fields.date('Needed By Date',required=True),
        'remarks': fields.text('Remarks',required=True), 
        'date_deadline': fields.date('Date Of Completion',required=True),
    }

