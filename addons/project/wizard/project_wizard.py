from lxml import etree
from openerp import tools
from openerp.tools.translate import _
from openerp.osv import fields, osv

class project_task_delegate(osv.osv_memory):

    def confirm_tasks(self, cr, uid,ids, context=None):
        for rec in self.browse(cr, uid,ids):
            tasks_id = self.pool.get('project.task').search(cr, uid, [('user_id','=',rec.name.id)], context=context)
            tasks_obj = self.pool.get('project.task').browse(cr, uid, tasks_id)
        for obj in tasks_obj:
            if obj.state == 'Draft':
                obj.state = 'In Progress'
            else:
                raise osv.except_osv(_('Not Allowed ! '),_('You can only change the record to IN progress state here !'))                
            return True
    
    def complete_tasks(self, cr, uid,ids, context=None):
        for rec in self.browse(cr, uid,ids):
            tasks_id = self.pool.get('project.task').search(cr, uid, [('user_id','=',rec.name.id)], context=context)
            tasks_obj = self.pool.get('project.task').browse(cr, uid, tasks_id)
        for obj in tasks_obj:
            if obj.state == 'In Progress':
                obj.state = 'Done'
            else:
                raise osv.except_osv(_('Not Allowed ! '),_('You can only change the record to Done state here !'))        
        return None
    
    
    _name = 'project.wizard.staterifts'
    _description = 'Project Bulk State Changes'
    _columns = {
        'name': fields.many2one('res.users', 'Performed By', required=True, help="User Who Perofrmed the Action"),
        'project_taks_id':fields.many2many('project.task', 'project_task_state_change_rel', 'task_id', 'parent_id',"Select Items"),                
    }

