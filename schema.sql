CREATE TYPE "role_code_type" AS ENUM (
  'ADMIN',
  'PROJECT_EDITOR',
  'PROJECT_VIEWER',
  'REPORT_EXPORTER_ALL'
);

CREATE TYPE "project_state_type" AS ENUM (
  'APPLICANTION_SHORT',
  'APPLICANTION_FULL',
  'DELETED',
  'ENDED',
  'FREEZE',
  'ARCHIVE',
  'PROJECT_IN_COMISSION',
  'PROJECT_ON_SUPPORT'
);

CREATE TYPE "support_type" AS ENUM (
  'FINANCE',
  'CREDIT',
  'EARTH',
  'EQUIP',
  'TECH'
);

CREATE TYPE "unit_type" AS ENUM (
  'RUB',
  'PIECES',
  'METERS',
  'METERS_CUBIC',
  'METERS_SQUARE',
  'HECTARES'
);

CREATE TYPE "programm_level_type" AS ENUM (
  'FEDERAL',
  'REGION',
  'MUNICIPAL'
);

CREATE TYPE "decision_type" AS ENUM (
  'EG',
  'MVK'
);

CREATE TABLE "user" (
  "id" int PRIMARY KEY,
  "last_name" text,
  "first_name" text,
  "middle_name" text,
  "email" text,
  "role_code" role_code_type
);

CREATE TABLE "district_id" (
  "id" int PRIMARY KEY,
  "name" text
);

CREATE TABLE "city" (
  "id" int PRIMARY KEY,
  "name" text
);

CREATE TABLE "project" (
  "id" int PRIMARY KEY,
  "owner_id" int,
  "address_id" int,
  "industry_id" int,
  "name" text,
  "application_own_amount" decimal,
  "application_support_amount" decimal,
  "work_place_count" int,
  "nalog_amount" int,
  "description" text,
  "state" project_state_type
);

CREATE TABLE "user_project" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "project_id" int
);

CREATE TABLE "business_org" (
  "id" int PRIMARY KEY,
  "address_id" int,
  "name" text,
  "name_short" text,
  "inn" text,
  "ogrn" text
);

CREATE TABLE "business_man" (
  "id" int PRIMARY KEY,
  "address_id" int,
  "last_name" text,
  "first_name" text,
  "middle_name" text,
  "inn" text,
  "ogrn" text
);

CREATE TABLE "owner" (
  "id" int PRIMARY KEY,
  "business_org_id" int,
  "business_man_id" int
);

CREATE TABLE "owner_contact" (
  "id" int PRIMARY KEY,
  "owner_id" int,
  "phone_no" text,
  "email" text
);

CREATE TABLE "support" (
  "id" int PRIMARY KEY,
  "project_id" int,
  "support_programm_id" int,
  "support_org_id" int,
  "date_start" date,
  "date_end" date,
  "type_code" support_type,
  "amount" decimal,
  "unit" unit_type,
  "desc" text
);

CREATE TABLE "support_programm" (
  "id" int PRIMARY KEY,
  "name" text,
  "active" boolean,
  "level_type_code" programm_level_type
);

CREATE TABLE "support_org" (
  "id" int PRIMARY KEY,
  "name" text
);

CREATE TABLE "address" (
  "id" int PRIMARY KEY,
  "district_id" int,
  "city_id" int,
  "post_code" text,
  "address" text
);

CREATE TABLE "decision" (
  "id" int PRIMARY KEY,
  "support_id" int,
  "decision_type" decision_type,
  "decision_date" date,
  "protocol_number" text,
  "decision" text
);

CREATE TABLE "industry" (
  "id" int PRIMARY KEY,
  "name" text
);

COMMENT ON TABLE "user" IS 'Пользователи системы';

COMMENT ON COLUMN "user"."last_name" IS 'Фамилия';

COMMENT ON COLUMN "user"."first_name" IS 'Имя';

COMMENT ON COLUMN "user"."middle_name" IS 'Отчество';

COMMENT ON COLUMN "user"."email" IS 'Адрес электронной почты';

COMMENT ON COLUMN "user"."role_code" IS 'Роль пользователя';

COMMENT ON TABLE "district_id" IS 'Справочник. Районы Сахалинской области';

COMMENT ON COLUMN "district_id"."name" IS 'Наименование района';

COMMENT ON TABLE "city" IS 'Справочник. Населенные пункты Сахалинской области';

COMMENT ON COLUMN "city"."name" IS 'Наименование населенного пункта';

COMMENT ON TABLE "project" IS 'Проект';

COMMENT ON COLUMN "project"."name" IS 'Название проекта';

COMMENT ON COLUMN "project"."application_own_amount" IS 'Собственная сумма. Заполняет сотрудник. Источник Клиент. По звонку или по заявлению';

COMMENT ON COLUMN "project"."application_support_amount" IS 'Запрашиваемая сумма. Заполняет сотрудник. Источник Клиент. По звонку или по заявлению';

COMMENT ON COLUMN "project"."work_place_count" IS 'Количество рабочих мест. Заполняет сотрудник. Источник Клиент. По звонку или по заявлению';

COMMENT ON COLUMN "project"."nalog_amount" IS 'Налоги, отчисляемые в бюджет. Заполняет сотрудник. Источник Клиент. По звонку или по заявлению';

COMMENT ON COLUMN "project"."description" IS 'Описание проекта. Заполняет сотрудник. Источник Клиент. По звонку или по заявлению';

COMMENT ON COLUMN "project"."state" IS 'Состояние проекта';

COMMENT ON TABLE "user_project" IS 'Связь пользователей системы с проектами';

COMMENT ON TABLE "business_org" IS 'Клиент - юридическое лицо';

COMMENT ON COLUMN "business_org"."name" IS 'Полное наименование';

COMMENT ON COLUMN "business_org"."name_short" IS 'Сокращенное наименование';

COMMENT ON COLUMN "business_org"."inn" IS 'ИНН';

COMMENT ON COLUMN "business_org"."ogrn" IS 'ОГРН';

COMMENT ON TABLE "business_man" IS 'Клиент - ИП или физическое лицо';

COMMENT ON COLUMN "business_man"."last_name" IS 'Фамилия';

COMMENT ON COLUMN "business_man"."first_name" IS 'Имя';

COMMENT ON COLUMN "business_man"."middle_name" IS 'Отчество';

COMMENT ON COLUMN "business_man"."inn" IS 'ИНН';

COMMENT ON COLUMN "business_man"."ogrn" IS 'ОГРН';

COMMENT ON TABLE "owner" IS 'Сущность владельца проектом';

COMMENT ON TABLE "owner_contact" IS 'Контакты владельца проектом';

COMMENT ON COLUMN "owner_contact"."phone_no" IS 'Номер телефона';

COMMENT ON COLUMN "owner_contact"."email" IS 'Адрес электронной почты';

COMMENT ON TABLE "support" IS 'Поддержка по проекту';

COMMENT ON COLUMN "support"."project_id" IS 'ID проекта к которому относится поддержка';

COMMENT ON COLUMN "support"."support_programm_id" IS 'ID государственной программы, по которой выделяется поддержка';

COMMENT ON COLUMN "support"."support_org_id" IS 'ID государственного органа, выделяющего поддержку';

COMMENT ON COLUMN "support"."date_start" IS 'Дата начала выделения поддержки';

COMMENT ON COLUMN "support"."date_end" IS 'Дата окончания выделения поддержки';

COMMENT ON COLUMN "support"."type_code" IS 'Вид поддержки';

COMMENT ON COLUMN "support"."amount" IS 'Размер поддержки';

COMMENT ON COLUMN "support"."unit" IS 'Единицы измерения';

COMMENT ON COLUMN "support"."desc" IS 'Описание';

COMMENT ON TABLE "support_programm" IS 'Справочник. Федеральные, региональные и муниципальные программы поддержки';

COMMENT ON COLUMN "support_programm"."name" IS 'Наименование программы';

COMMENT ON COLUMN "support_programm"."active" IS 'Признак активности программы';

COMMENT ON COLUMN "support_programm"."level_type_code" IS 'Уровень программы';

COMMENT ON TABLE "support_org" IS 'Справочник. Министерство, ведомство, оказывающее поддержку';

COMMENT ON TABLE "address" IS 'Адреса';

COMMENT ON COLUMN "address"."post_code" IS 'Почтовый индекс';

COMMENT ON COLUMN "address"."address" IS 'Улица, дом, квартира, офис';

COMMENT ON TABLE "decision" IS 'Решения о выделении поддержки';

COMMENT ON COLUMN "decision"."decision_type" IS 'Вид решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии"';

COMMENT ON COLUMN "decision"."decision_date" IS 'Дата создания решения. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии';

COMMENT ON COLUMN "decision"."protocol_number" IS 'Номер протокола. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии';

COMMENT ON COLUMN "decision"."decision" IS 'Решение. Заполняет сотрудник. Источник протокол заседания. По итогам проведения комиссии';

COMMENT ON TABLE "industry" IS 'Справочник. Отрасли экономики';

COMMENT ON COLUMN "industry"."name" IS 'Наименование индустрии';

ALTER TABLE "project" ADD FOREIGN KEY ("owner_id") REFERENCES "owner" ("id");

ALTER TABLE "support" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("id");

ALTER TABLE "owner_contact" ADD FOREIGN KEY ("owner_id") REFERENCES "owner" ("id");

ALTER TABLE "project" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("id");

ALTER TABLE "owner" ADD FOREIGN KEY ("business_org_id") REFERENCES "business_org" ("id");

ALTER TABLE "owner" ADD FOREIGN KEY ("business_man_id") REFERENCES "business_man" ("id");

ALTER TABLE "support" ADD FOREIGN KEY ("support_org_id") REFERENCES "support_org" ("id");

ALTER TABLE "support" ADD FOREIGN KEY ("support_programm_id") REFERENCES "support_programm" ("id");

ALTER TABLE "decision" ADD FOREIGN KEY ("support_id") REFERENCES "support" ("id");

ALTER TABLE "project" ADD FOREIGN KEY ("industry_id") REFERENCES "industry" ("id");

ALTER TABLE "address" ADD FOREIGN KEY ("district") REFERENCES "district" ("id");

ALTER TABLE "address" ADD FOREIGN KEY ("city_id") REFERENCES "city" ("id");

ALTER TABLE "business_man" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("id");

ALTER TABLE "business_org" ADD FOREIGN KEY ("address_id") REFERENCES "address" ("id");

ALTER TABLE "user_project" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "user_project" ADD FOREIGN KEY ("project_id") REFERENCES "project" ("id");
