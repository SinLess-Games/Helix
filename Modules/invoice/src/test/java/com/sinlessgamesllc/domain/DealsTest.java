package com.sinlessgamesllc.domain;

import static org.assertj.core.api.Assertions.assertThat;

import com.sinlessgamesllc.web.rest.TestUtil;
import org.junit.jupiter.api.Test;

class DealsTest {

    @Test
    void equalsVerifier() throws Exception {
        TestUtil.equalsVerifier(Deals.class);
        Deals deals1 = new Deals();
        deals1.setId(1L);
        Deals deals2 = new Deals();
        deals2.setId(deals1.getId());
        assertThat(deals1).isEqualTo(deals2);
        deals2.setId(2L);
        assertThat(deals1).isNotEqualTo(deals2);
        deals1.setId(null);
        assertThat(deals1).isNotEqualTo(deals2);
    }
}
