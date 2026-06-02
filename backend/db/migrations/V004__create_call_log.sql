-- ============================================================
-- 外呼流水表 DDL
-- 版本: V004
-- 说明: 记录平台发起的每一次外呼记录及通话结果
--       CALL_RESULT 枚举: 接通 / 未接 / 拒接空号
--       跟进状态由最近一次 CALL_RESULT 推导:
--         最新记录为"接通"   => 已接通
--         最新记录为其他值   => 未接通
--         无任何记录         => 未跟进
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE custgroup.T_CALL_LOG
(
    ID             NUMBER          NOT NULL,              -- 主键
    CLIENT_ID      VARCHAR2(20)    NOT NULL,              -- 客户资金账号
    BRANCH_NO      VARCHAR2(10)    NOT NULL,              -- 营业部编号
    LOGIN_ID       VARCHAR2(20)    NOT NULL,              -- 外呼员工OA
    EMP_NAME       VARCHAR2(50),                          -- 外呼员工姓名
    CALL_TIME      TIMESTAMP       NOT NULL,              -- 外呼发起时间
    CALL_RESULT    VARCHAR2(10)    NOT NULL,              -- 通话结果: 接通/未接/拒接空号
    CALL_DURATION  NUMBER(6)       DEFAULT 0,             -- 通话时长，单位秒，接通时有效
    REMARK         VARCHAR2(500),                         -- 备注
    CREATE_TIME    TIMESTAMP       DEFAULT LOCALTIMESTAMP, -- 记录创建时间
    CONSTRAINT PK_CALL_LOG PRIMARY KEY (ID),
    CONSTRAINT CK_CALL_RESULT CHECK (CALL_RESULT IN ('接通', '未接', '拒接空号'))
);

COMMENT ON TABLE  custgroup.T_CALL_LOG                  IS '外呼流水表，记录平台每次外呼及通话结果';
COMMENT ON COLUMN custgroup.T_CALL_LOG.ID               IS '主键';
COMMENT ON COLUMN custgroup.T_CALL_LOG.CLIENT_ID        IS '客户资金账号';
COMMENT ON COLUMN custgroup.T_CALL_LOG.BRANCH_NO        IS '营业部编号';
COMMENT ON COLUMN custgroup.T_CALL_LOG.LOGIN_ID         IS '外呼员工OA';
COMMENT ON COLUMN custgroup.T_CALL_LOG.EMP_NAME         IS '外呼员工姓名';
COMMENT ON COLUMN custgroup.T_CALL_LOG.CALL_TIME        IS '外呼发起时间';
COMMENT ON COLUMN custgroup.T_CALL_LOG.CALL_RESULT      IS '通话结果: 接通, 未接, 拒接空号';
COMMENT ON COLUMN custgroup.T_CALL_LOG.CALL_DURATION    IS '通话时长，单位秒，接通时有效';
COMMENT ON COLUMN custgroup.T_CALL_LOG.REMARK           IS '备注';
COMMENT ON COLUMN custgroup.T_CALL_LOG.CREATE_TIME      IS '记录创建时间';


-- ------------------------------------------------------------
-- 2. 主键序列
-- ------------------------------------------------------------
CREATE SEQUENCE custgroup.SEQ_CALL_LOG
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;


-- ------------------------------------------------------------
-- 3. 触发器：INSERT 时自动填充 ID
-- ------------------------------------------------------------
CREATE OR REPLACE TRIGGER custgroup.TRG_CALL_LOG_ID
    BEFORE INSERT ON custgroup.T_CALL_LOG
    FOR EACH ROW
BEGIN
    IF :NEW.ID IS NULL THEN
        :NEW.ID := custgroup.SEQ_CALL_LOG.NEXTVAL;
    END IF;
END;
/


-- ------------------------------------------------------------
-- 4. 索引
-- ------------------------------------------------------------

-- 跟进状态查询：按营业部取各客户最新一条记录（CALL_TIME DESC）
CREATE INDEX IDX_CL_BRANCH_CLIENT_TIME
    ON custgroup.T_CALL_LOG (BRANCH_NO, CLIENT_ID, CALL_TIME DESC);

-- 按员工查外呼记录（绩效/报表场景）
CREATE INDEX IDX_CL_LOGIN_ID
    ON custgroup.T_CALL_LOG (LOGIN_ID, CALL_TIME DESC);
