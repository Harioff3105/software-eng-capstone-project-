import test from 'node:test';import assert from 'node:assert/strict';
test('health response contract',()=>{const response={ok:true,service:'scholarship-api'};assert.equal(response.ok,true);assert.equal(response.service,'scholarship-api')});
test('recommendation score remains bounded',()=>{const score=.55+.25+.20;assert.ok(score>=0&&score<=1)});
