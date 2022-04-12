package com.sinlessgamesllc.repository;

import com.sinlessgamesllc.domain.Deals;
import org.springframework.data.jpa.repository.*;
import org.springframework.stereotype.Repository;

/**
 * Spring Data SQL repository for the Deals entity.
 */
@SuppressWarnings("unused")
@Repository
public interface DealsRepository extends JpaRepository<Deals, Long> {}
