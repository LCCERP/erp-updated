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
    
    def complete_tasks(self, cr, uid,ids, context=None):
        ids_list = []
        for rec in self.browse(cr, uid,ids):
            for idd in rec.project_taks_id:
                ids_list.append(idd.id)
            tasks_id = self.pool.get('project.task').search(cr, uid, [('id','in',ids_list),('state','=','In Progress')], context=context)
            tasks_obj = self.pool.get('project.task').browse(cr, uid, tasks_id)
        for obj in tasks_obj:
            self.pool.get('project.task').write(cr,uid,obj.id,{'state':'Done'},context)
            self.pool.get('project.task.custom').create(cr, uid, {
                                                               'name':obj.name,
                                                               'shipment_no': obj.shipment_no,
                                                               'project_id':obj.project_id.id,
                                                               'huawei_project_name': obj.huawei_project_name,
                                                               'po_no': obj.po_no,
                                                               'reviewer_id':obj.reviewer_id.id,
                                                               'po_line_no':obj.po_line_no,
                                                               'province':obj.province,
                                                               'unit':obj.unit,
                                                               'unite_price': obj.unite_price,
                                                               'po_value':  obj.po_value,
                                                               'start_date':  obj.start_date,
                                                               'needed_by_date':obj.needed_by_date,
                                                               'remarks': obj.remarks,
                                                               'description': obj.description,
                                                               'date_deadline': obj.date_deadline,
                                                               'user_id': obj.user_id.id,
                                                               'state': 'Done'
                                                               },context=context)
        return None
    
    _name = 'project.wizard.staterifts'
    _description = 'Project Bulk State Changes'
    _columns = {
        'project_taks_id':fields.many2many('project.task', 'project_task_state_change_rel', 'task_id', 'parent_id',"Select Items"),                
    }

