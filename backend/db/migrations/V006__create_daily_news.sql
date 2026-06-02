-- ============================================================
-- 每日资讯表 DDL
-- 版本: V006
-- 说明: 存储每日推送给营销人员的市场/政策等资讯
--       CATEGORY 枚举: 市场 / 政策 / 产品 / 公司 / 宏观
-- ============================================================


-- ------------------------------------------------------------
-- 1. 主表
-- ------------------------------------------------------------
CREATE TABLE CUSTGROUP.AIPC_DAILY_NEWS
(
    NEWS_ID      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    TITLE        VARCHAR2(200)  NOT NULL,                           -- 资讯标题
    CATEGORY     VARCHAR2(20)   NOT NULL,                           -- 资讯分类
    LINK         VARCHAR2(500),                                     -- 原文链接（可为空）
    NEWS_DATE    DATE           NOT NULL,                           -- 资讯日期
    CREATE_TIME  TIMESTAMP      DEFAULT SYSTIMESTAMP NOT NULL       -- 录入时间
);

COMMENT ON TABLE  CUSTGROUP.AIPC_DAILY_NEWS             IS '每日资讯表，存储推送给营销人员的市场/政策资讯';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.NEWS_ID     IS '主键，自增';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.TITLE       IS '资讯标题';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.CATEGORY    IS '资讯分类: 市场/政策/产品/公司/宏观';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.LINK        IS '原文链接，可为空';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.NEWS_DATE   IS '资讯日期';
COMMENT ON COLUMN CUSTGROUP.AIPC_DAILY_NEWS.CREATE_TIME IS '录入时间';


-- ------------------------------------------------------------
-- 2. 索引
-- ------------------------------------------------------------

-- 按日期降序查最新资讯（今日banner + 弹窗默认排序）
CREATE INDEX IDX_DN_DATE
    ON CUSTGROUP.AIPC_DAILY_NEWS (NEWS_DATE DESC);

-- 按分类过滤
CREATE INDEX IDX_DN_CATEGORY
    ON CUSTGROUP.AIPC_DAILY_NEWS (CATEGORY, NEWS_DATE DESC);


-- ------------------------------------------------------------
-- 3. 初始化示例数据（可删除）
-- ------------------------------------------------------------
INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('央行发布二季度货币政策报告，稳息基调不变', '市场', NULL, TRUNC(SYSDATE));

INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('个人养老金账户缴存规则调整，年度上限升至2.4万', '政策', NULL, TRUNC(SYSDATE));

INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('沪深300指数成分股季度调整结果公布', '市场', NULL, TRUNC(SYSDATE));

INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('公募基金费率改革二期落地，管理费上限下调', '产品', NULL, TRUNC(SYSDATE));

INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('美联储5月议息会议：维持利率不变，关注通胀路径', '宏观', NULL, TRUNC(SYSDATE) - 1);

INSERT INTO CUSTGROUP.AIPC_DAILY_NEWS (TITLE, CATEGORY, LINK, NEWS_DATE)
VALUES ('证监会：进一步推进注册制改革完善配套机制', '政策', NULL, TRUNC(SYSDATE) - 1);

COMMIT;
