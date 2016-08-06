from lxml import etree
from openerp import tools
from openerp.tools.translate import _
from openerp.osv import fields, osv

class project_task_delegate(osv.osv_memory):

    def confirm_tasks(self, cr, uid,ids, context=None):
        ids_list = []
        for rec in self.browse(cr, uid,ids):
            for idd in rec.project_taks_id:
                ids_list.append(idd.id)
            tasks_id = self.pool.get('project.task').search(cr, uid, [('id','in',ids_list),('state','=','Draft')], context=context)
            tasks_obj = self.pool.get('project.task').browse(cr, uid, tasks_id)
        for obj in tasks_obj:
            self.pool.get('project.task').write(cr,uid,obj.id,{'state':'In Progress'},context)
        return None
        
    _name = 'project.wizard.staterifts'
    _description = 'Project Bulk State Changes'
    _columns = {
        'project_taks_id':fields.many2many('project.task', 'project_task_state_change_rel', 'task_id', 'parent_id',"Select Items"),                
    }

