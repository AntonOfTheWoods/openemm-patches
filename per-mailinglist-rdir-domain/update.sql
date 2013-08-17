/* Add an rdir_domain to the mailinglist_tbl */

alter table mailinglist_tbl add column `rdir_domain` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '';
alter table mailinglist_tbl add column `messageid_domain` varchar(255) COLLATE utf8_unicode_ci NOT NULL DEFAULT '';

