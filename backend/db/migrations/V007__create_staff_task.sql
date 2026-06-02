-- ============================================================
-- 营销人员任务表 DDL
-- 版本: V007
-- 说明: 存储每位营销人员的日常任务
--
-- TASK_TYPE（一级分类）枚举:
--   建联类 / 跟进类 / 周期类 / 营销活动类 / 合规类
--
-- TASK_SUB_TYPE（子类）枚举:
--   建联类     → AI外呼 / 人工外呼 / 加微信 / 绑定开户
--   跟进类     → 意向跟进 / 逾期未回复 / 到期提醒 / 重点二次触达
--   周期类     → 引客 / 养客 / 复投 / 流失预警
--   营销活动类 → 【动态活动名称，由总部统一下发，如"五月财富节""基金定投推广季"等，不做枚举约束】
--   合规类     → 录音复盘 / 风险测评到期 / 培训作业
--
-- PRIORITY（优先级）枚举: 高 / 中 / 低
-- SOURCE（来源）枚举:  系统自动 / 主管下发
-- STATUS（状态）枚举:  待处理 / 处理中 / 已完成 / 已逾期
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE CUSTGROUP.AIPC_STAFF_TASK
(
    TASK_ID       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    LOGIN_ID      VARCHAR2(20)    NOT NULL,                              -- 员工OA
    EMP_NAME      VARCHAR2(50),                                          -- 员工姓名
    TASK_TYPE     VARCHAR2(20)    NOT NULL,                              -- 一级分类
    TASK_SUB_TYPE VARCHAR2(20)    NOT NULL,                              -- 子类
    TASK_NAME     VARCHAR2(200)   NOT NULL,                              -- 任务名称/描述
    PRIORITY      VARCHAR2(5)     DEFAULT '中' NOT NULL,                 -- 优先级: 高/中/低
    SOURCE        VARCHAR2(10)    DEFAULT '系统自动' NOT NULL,           -- 来源: 系统自动/主管下发
    ISSUE_DATE    DATE            DEFAULT TRUNC(SYSDATE) NOT NULL,       -- 下发日期
    DUE_DATE      DATE            NOT NULL,                              -- 截止日期
    STATUS        VARCHAR2(10)    DEFAULT '待处理' NOT NULL,             -- 状态
    FINISH_DATE   DATE,                                                  -- 完成日期（完成后填入）
    CUST_NO       VARCHAR2(20),                                          -- 关联客户资金账号（可空）
    REMARK        VARCHAR2(500),                                         -- 备注
    CREATE_TIME   TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,         -- 创建时间
    UPDATE_TIME   TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,         -- 最后更新时间

    CONSTRAINT CK_TASK_TYPE     CHECK (TASK_TYPE IN ('建联类', '跟进类', '周期类', '营销活动类', '合规类')),
    CONSTRAINT CK_TASK_PRIORITY CHECK (PRIORITY IN ('高', '中', '低')),
    CONSTRAINT CK_TASK_SOURCE   CHECK (SOURCE IN ('系统自动', '主管下发')),
    CONSTRAINT CK_TASK_STATUS   CHECK (STATUS IN ('待处理', '处理中', '已完成', '已逾期'))
);

COMMENT ON TABLE  CUSTGROUP.AIPC_STAFF_TASK               IS '营销人员任务表';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.TASK_ID       IS '主键，自增';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.LOGIN_ID      IS '员工OA号';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.EMP_NAME      IS '员工姓名';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.TASK_TYPE     IS '一级分类: 建联类/跟进类/周期类/合规类';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.TASK_SUB_TYPE IS '子类。建联/跟进/周期/合规类按固定枚举；营销活动类存活动名称（动态，由总部下发时写入）';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.TASK_NAME     IS '任务名称或具体描述';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.PRIORITY      IS '优先级: 高/中/低';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.SOURCE        IS '任务来源: 系统自动/主管下发';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.ISSUE_DATE    IS '下发日期';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.DUE_DATE      IS '截止日期';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.STATUS        IS '完成情况: 待处理/处理中/已完成/已逾期';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.FINISH_DATE   IS '实际完成日期，完成后填入';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.CUST_NO       IS '关联客户资金账号，合规类任务可为空';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.REMARK        IS '备注';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.CREATE_TIME   IS '记录创建时间';
COMMENT ON COLUMN CUSTGROUP.AIPC_STAFF_TASK.UPDATE_TIME   IS '记录最后更新时间';


-- ------------------------------------------------------------
-- 2. 索引
-- ------------------------------------------------------------

-- 员工任务列表（最常用：按员工+状态查，按截止日期排序）
CREATE INDEX IDX_ST_LOGIN_STATUS
    ON CUSTGROUP.AIPC_STAFF_TASK (LOGIN_ID, STATUS, DUE_DATE ASC);

-- 按下发日期查当日任务（工作台总览统计用）
CREATE INDEX IDX_ST_LOGIN_ISSUE
    ON CUSTGROUP.AIPC_STAFF_TASK (LOGIN_ID, ISSUE_DATE DESC);

-- 逾期扫描（定时任务用：找所有超期未完成的记录批量置为已逾期）
CREATE INDEX IDX_ST_DUE_STATUS
    ON CUSTGROUP.AIPC_STAFF_TASK (DUE_DATE, STATUS);


-- ------------------------------------------------------------
-- 3. 逾期自动更新触发器
--    每次 UPDATE 时，若 DUE_DATE < SYSDATE 且 STATUS 仍为 待处理/处理中，
--    则自动置为 已逾期（业务上也可改由定时批处理来做，触发器仅作兜底）
-- ------------------------------------------------------------
CREATE OR REPLACE TRIGGER CUSTGROUP.TRG_STAFF_TASK_OVERDUE
    BEFORE UPDATE ON CUSTGROUP.AIPC_STAFF_TASK
    FOR EACH ROW
BEGIN
    -- 更新时间戳
    :NEW.UPDATE_TIME := SYSTIMESTAMP;
    -- 若截止日已过且尚未完成，则标记逾期
    IF :NEW.DUE_DATE < TRUNC(SYSDATE)
       AND :NEW.STATUS IN ('待处理', '处理中')
    THEN
        :NEW.STATUS := '已逾期';
    END IF;
END;
/


-- ------------------------------------------------------------
-- 4. 示例数据（可按需删除）
-- ------------------------------------------------------------
INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '建联类', 'AI外呼',   'AI外呼推荐客户：陈*兰，建议加微',          '高', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '跟进类', '意向跟进',  'S级客户意向跟进：建联中，截止今日10:00',   '高', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '待处理', 'C001001');

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '跟进类', '逾期未回复', '逾期提醒：赵*加微3天未回复，建议电话跟进', '高', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '待处理', 'C001002');

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '周期类', '养客',       '持仓关怀跟进：5位持仓客户本周触达',         '中', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE)+2,   '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '周期类', '复投',       '到期客户转化：2位产品到期客户需再营销',     '中', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE)+3,   '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '合规类', '录音复盘',   '昨日3条外呼录音待质检确认',                 '中', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '建联类', '人工外呼',   '重点客户人工跟进：李*华，资产500W+',        '中', '主管下发', TRUNC(SYSDATE), TRUNC(SYSDATE)+1,   '处理中', 'C001003');

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '周期类', '引客',       '新客专属欢迎：3位新开户客户完成首次触达',   '低', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE)+7,   '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '合规类', '培训作业',   'AI辅助外呼2.0新功能线上宣导学习',           '低', '主管下发', TRUNC(SYSDATE), TRUNC(SYSDATE)+1,   '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '营销活动类', '五月财富节',     '五月财富节：邀约名下高净值客户参与线上直播活动',  '高', '主管下发', TRUNC(SYSDATE), TRUNC(SYSDATE)+5,  '待处理', NULL);

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, CUST_NO)
VALUES ('oa001', '张超越', '营销活动类', '基金定投推广季', '基金定投推广季：向持仓客户推介定投计划，确认意向', '中', '主管下发', TRUNC(SYSDATE), TRUNC(SYSDATE)+3,  '处理中', NULL);

-- 已完成示例
INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, FINISH_DATE, CUST_NO)
VALUES ('oa001', '张超越', '建联类', '加微信',     '客户王*芳微信添加成功',                     '中', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '已完成', TRUNC(SYSDATE), 'C001004');

INSERT INTO CUSTGROUP.AIPC_STAFF_TASK
    (LOGIN_ID, EMP_NAME, TASK_TYPE, TASK_SUB_TYPE, TASK_NAME, PRIORITY, SOURCE, ISSUE_DATE, DUE_DATE, STATUS, FINISH_DATE, CUST_NO)
VALUES ('oa001', '张超越', '周期类', '流失预警',   '流失预警处理：刘*完成电话挽留',             '高', '系统自动', TRUNC(SYSDATE), TRUNC(SYSDATE),     '已完成', TRUNC(SYSDATE), 'C001005');

COMMIT;
