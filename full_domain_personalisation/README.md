Introduction
============

These patches:

 * give each mailing list the possibility to have a different redirect domain and message-id.

If they do not have one then the default company_tbl value will be used for rdir_domain and the mailloop_domain for the message-id.
If the company_tbl does not have a mailloop_domain then it will fall back on the original mailgun.ini.domain value from emm.properties
The values must currently be maintained manually directly in the DB, much like if you want to change the company redirect.

This should be backwards-compatible with any existing configuration

 * make it possible to configure a List-Unsubscribe for each sender domain

The changes simply extend the existing system to allow for variable values keyed on the sender address' domain and adds mailto
This should be backwards compatible with any existing configuration