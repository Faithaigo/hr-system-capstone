from auditlog.models import AuditLog


def add_audit_log(actor, action, model, record_id):
    """
    Log actions like saving, deleting, updating
    :param actor:
    :param action:
    :param model:
    :param record_id:
    :return:
    """
    AuditLog.objects.create(actor=actor,
                            action=action,
                            model=model,
                            record_id=record_id)
